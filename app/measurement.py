"""Own calibrated distances, closed perimeters and simple polygon areas."""
import math

UNITS_MM={'mm':1.0,'cm':10.0,'m':1000.0,'in':25.4,'ft':304.8}
MAX_POINTS=512


def snap_point(point,reference=None,grid=0,angle_step=0):
    """Explicit PDF-point grid and angular constraint; no invisible vector guess."""
    import math
    point=points([point],1)[0]
    if any(type(v) not in (int,float) or not math.isfinite(v) for v in (grid,angle_step)) or not 0<=grid<=1000 or not 0<=angle_step<=180:
        raise ValueError('Grade0–1000pt e restrição angular0–180graus.')
    x,y=point
    if reference is not None and angle_step:
        origin=points([reference],1)[0];dx,dy=x-origin[0],y-origin[1];radius=math.hypot(dx,dy)
        step=math.radians(angle_step);angle=round(math.atan2(dy,dx)/step)*step
        x,y=origin[0]+radius*math.cos(angle),origin[1]+radius*math.sin(angle)
    elif grid:x,y=round(x/grid)*grid,round(y/grid)*grid
    return x,y


def points(value,minimum=2):
    if not isinstance(value,list) or not minimum<=len(value)<=MAX_POINTS:
        raise ValueError('Quantidade de pontos inválida; máximo512.')
    result=[]
    for point in value:
        if (not isinstance(point,(list,tuple)) or len(point)!=2 or
                not all(type(v) in (int,float) and math.isfinite(v) and abs(v)<=2000000 for v in point)):
            raise ValueError('Coordenadas de medição inválidas.')
        result.append(tuple(point))
    if any(a==b for a,b in zip(result,result[1:])):raise ValueError('Pontos consecutivos repetidos.')
    return result


def calibrated_scale(reference,known_length,unit='cm'):
    reference=points(reference)
    if len(reference)!=2 or unit not in UNITS_MM or type(known_length) not in (int,float) or not math.isfinite(known_length) or not 0<known_length<=1e12:
        raise ValueError('Referência de calibração inválida.')
    distance=math.dist(*reference)
    if distance<=0:raise ValueError('Referência sem comprimento.')
    return known_length*UNITS_MM[unit]/distance


def _intersects(a,b,c,d):
    def orient(p,q,r):return (q[0]-p[0])*(r[1]-p[1])-(q[1]-p[1])*(r[0]-p[0])
    def on(p,q,r):return min(p[0],q[0])<=r[0]<=max(p[0],q[0]) and min(p[1],q[1])<=r[1]<=max(p[1],q[1])
    x,y,z,w=orient(a,b,c),orient(a,b,d),orient(c,d,a),orient(c,d,b)
    return (x*y<0 and z*w<0) or (x==0 and on(a,b,c)) or (y==0 and on(a,b,d)) or (z==0 and on(c,d,a)) or (w==0 and on(c,d,b))


def measure(value,kind='distance',unit='cm',mm_per_point=25.4/72):
    coords=points(value,3 if kind=='area' else 2)
    if unit not in UNITS_MM or type(mm_per_point) not in (int,float) or not math.isfinite(mm_per_point) or not 0<mm_per_point<=1e12:
        raise ValueError('Unidade ou escala inválida.')
    factor=mm_per_point/UNITS_MM[unit]
    if kind=='distance':
        if len(coords)!=2:raise ValueError('Distância exige exatamente2 pontos.')
        return math.dist(*coords)*factor
    if kind=='perimeter':return math.fsum(math.dist(a,b) for a,b in zip(coords,coords[1:]+coords[:1]))*factor
    if kind!='area':raise ValueError('Tipo de medição inválido.')
    if coords[0]==coords[-1]:coords.pop()
    if len(coords)<3:raise ValueError('Área exige3 vértices distintos.')
    edges=list(zip(coords,coords[1:]+coords[:1]))
    for i,(a,b) in enumerate(edges):
        for j in range(i+1,len(edges)):
            if j==i+1 or i==0 and j==len(edges)-1:continue
            if _intersects(a,b,*edges[j]):raise ValueError('Polígono com interseção; área ambígua.')
    x0,y0=coords[0];translated=[(x-x0,y-y0) for x,y in coords]
    area=abs(math.fsum(a[0]*b[1]-b[0]*a[1] for a,b in zip(translated,translated[1:]+translated[:1])))/2
    if area==0:raise ValueError('Polígono sem área.')
    return area*factor*factor
