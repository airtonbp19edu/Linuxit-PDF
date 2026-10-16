#!/usr/bin/env python3
"""Verify a real remote HEAD and save a receipt outside the working tree."""
import argparse,json,subprocess
from pathlib import Path
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--receipt',type=Path,required=True)
args=parser.parse_args();root=Path(__file__).resolve().parents[1]
if args.receipt.resolve().is_relative_to(root):parser.error('Receipt must be outside the checkout so verification cannot dirty its own result')
def git(*parts):return subprocess.check_output(['git',*parts],cwd=root,text=True).strip()
branch=git('branch','--show-current')
local=git('rev-parse','HEAD');remote=git('ls-remote','origin','refs/heads/'+branch).split()[0]
changes=git('status','--porcelain')
report={'branch':branch,'local_head':local,'confirmed_remote_head':remote,'worktree_clean':not changes,
        'synchronized':local==remote and not changes,'publicable_tracked_artifacts_percent':100 if local==remote and not changes else None,
        'method':'Real ls-remote HEAD comparison and empty git status; ignored staging/caches and restricted original materials are not publicable artifacts.'}
args.receipt.parent.mkdir(parents=True,exist_ok=True);args.receipt.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
raise SystemExit(0 if report['synchronized'] else 1)
