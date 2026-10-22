"""Bounded, offline OCSP decisions for an explicitly anchored certificate chain.

No URL discovery or requests. Both CertID hashes, serial, signature, responder
authorization and freshness must match. DSS certificates are helpers, never roots.
"""
from datetime import timedelta


def _valid(cert, moment):
    return cert.not_valid_before_utc <= moment <= cert.not_valid_after_utc


def _issued(child, parent):
    try:
        child.verify_directly_issued_by(parent)
        return True
    except (ValueError, TypeError):
        return False
    except Exception:
        return False


def _signature(key, signature, message, algorithm, parameters=None):
    from cryptography.hazmat.primitives.asymmetric import rsa, ec, padding, dsa, ed25519, ed448
    try:
        if isinstance(key, rsa.RSAPublicKey):
            key.verify(signature, message, parameters or padding.PKCS1v15(), algorithm)
        elif isinstance(key, ec.EllipticCurvePublicKey):
            key.verify(signature, message, ec.ECDSA(algorithm))
        elif isinstance(key, dsa.DSAPublicKey):
            key.verify(signature, message, algorithm)
        elif isinstance(key, (ed25519.Ed25519PublicKey, ed448.Ed448PublicKey)):
            key.verify(signature, message)
        else:
            return False
        return True
    except Exception:
        return False


def _one_response(raw, cert, issuer, moment):
    from cryptography import x509
    from cryptography.x509 import ocsp
    from cryptography.hazmat.primitives import hashes
    from cryptography.x509.oid import ExtendedKeyUsageOID
    try:
        response = ocsp.load_der_ocsp_response(raw)
        if response.response_status != ocsp.OCSPResponseStatus.SUCCESSFUL:
            return None
        # A bounded SingleResponse profile; a multi-response DER is refused rather
        # than accidentally matching a different serial in the same response.
        singles = list(response.responses)
        if len(singles) != 1:
            return None
        single = singles[0]
        expected = ocsp.OCSPRequestBuilder().add_certificate(cert, issuer, single.hash_algorithm).build()
        if (single.serial_number != expected.serial_number or
                single.issuer_name_hash != expected.issuer_name_hash or
                single.issuer_key_hash != expected.issuer_key_hash):
            return None
        next_update = single.next_update_utc
        if (next_update is None or not single.this_update_utc <= moment <= next_update or
                response.produced_at_utc > moment + timedelta(minutes=5)):
            return None
        candidates = [issuer] + list(response.certificates)
        if len(candidates) > 17:
            return None
        for responder in candidates:
            if response.responder_name is not None:
                match = responder.subject == response.responder_name
            else:
                match = x509.SubjectKeyIdentifier.from_public_key(responder.public_key()).digest == response.responder_key_hash
            if not match or not _valid(responder, moment):
                continue
            is_issuer = responder.fingerprint(hashes.SHA256()) == issuer.fingerprint(hashes.SHA256())
            if not is_issuer:
                if not _issued(responder, issuer):
                    continue
                try:
                    if ExtendedKeyUsageOID.OCSP_SIGNING not in responder.extensions.get_extension_for_class(x509.ExtendedKeyUsage).value:
                        continue
                    # A delegated responder otherwise needs its own revocation
                    # path. This bounded offline profile supports only no-check
                    # delegates; it never silently ignores that obligation.
                    responder.extensions.get_extension_for_class(x509.OCSPNoCheck)
                except x509.ExtensionNotFound:
                    continue
            try:
                if not responder.extensions.get_extension_for_class(x509.KeyUsage).value.digital_signature:
                    continue
            except x509.ExtensionNotFound:
                pass
            if _signature(responder.public_key(), response.signature, response.tbs_response_bytes,
                          response.signature_hash_algorithm):
                return single.certificate_status.name.lower()
    except (ValueError, TypeError, AttributeError, NotImplementedError):
        return None
    return None


def verify_ocsp_chain(signers, helpers, anchors, responses, moment):
    """Return an OCSP result for every non-anchor certificate of every signer path.

    This complements an independent CMS/OpenSSL chain check. Missing, ambiguous,
    unsupported or stale material never becomes a positive revocation decision.
    """
    from cryptography import x509
    from cryptography.hazmat.primitives import hashes
    unique = {c.fingerprint(hashes.SHA256()): c for c in list(helpers) + list(anchors)}
    roots = {c.fingerprint(hashes.SHA256()) for c in anchors}
    decisions = []
    for signer in signers:
        current = signer; seen = set()
        for _ in range(16):
            digest = current.fingerprint(hashes.SHA256())
            if digest in roots:
                break
            if digest in seen or not _valid(current, moment):
                decisions.append(dict(serial=str(current.serial_number), status='unknown'));break
            seen.add(digest)
            issuers = []
            for candidate in unique.values():
                if not _valid(candidate, moment) or not _issued(current, candidate):
                    continue
                try:
                    if not candidate.extensions.get_extension_for_class(x509.BasicConstraints).value.ca:
                        continue
                    try:
                        if not candidate.extensions.get_extension_for_class(x509.KeyUsage).value.key_cert_sign:
                            continue
                    except x509.ExtensionNotFound:
                        pass
                except x509.ExtensionNotFound:
                    continue
                issuers.append(candidate)
            if len(issuers) != 1:
                decisions.append(dict(serial=str(current.serial_number), status='unknown'));break
            issuer = issuers[0]
            statuses = [_one_response(raw, current, issuer, moment) for raw in responses]
            status = 'revoked' if 'revoked' in statuses else 'good' if 'good' in statuses else 'unknown'
            decisions.append(dict(serial=str(current.serial_number), status=status))
            current = issuer
        else:
            decisions.append(dict(serial=str(current.serial_number), status='unknown'))
    return dict(verified=bool(decisions) and all(d['status'] == 'good' for d in decisions),
                revoked=any(d['status'] == 'revoked' for d in decisions), decisions=decisions,
                network_used=False, profile='single-response issuer or directly delegated OCSP; all non-anchor certificates')
