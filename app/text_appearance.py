"""Shape Unicode annotation text with Pango/Cairo in the limited worker."""
import base64,io,math


def build_text_appearance(request):
    if (not isinstance(request,dict) or set(request)!={'text','width','height','stamp'}
            or not isinstance(request['text'],str) or not 1<=len(request['text'])<=4096
            or type(request['stamp']) is not bool
            or not all(type(request[k]) in (int,float) and math.isfinite(request[k]) and 2<=request[k]<=20000 for k in ('width','height'))):
        raise ValueError('Texto ou área da aparência inválidos.')
    import cairo,gi
    gi.require_version('Pango','1.0');gi.require_version('PangoCairo','1.0')
    from gi.repository import Pango,PangoCairo
    output=io.BytesIO();w,h=request['width'],request['height']
    surface=cairo.PDFSurface(output,w,h);context=cairo.Context(surface)
    context.rectangle(0,0,w,h);context.clip();context.set_source_rgb(.85,.1,.1)
    padding=min(4,w/10,h/10)
    if request['stamp']:
        context.set_line_width(min(2,w/20,h/20));context.rectangle(padding,padding,w-2*padding,h-2*padding);context.stroke();padding*=2
    layout=PangoCairo.create_layout(context);layout.set_text(request['text'],-1)
    font=Pango.FontDescription('DejaVu Sans');font.set_absolute_size(12*Pango.SCALE);layout.set_font_description(font)
    layout.set_width(max(1,round((w-2*padding)*Pango.SCALE)));layout.set_wrap(Pango.WrapMode.WORD_CHAR)
    context.move_to(padding,padding);PangoCairo.show_layout(context,layout)
    context.show_page();surface.finish();raw=output.getvalue()
    if len(raw)>4*1024**2:raise ValueError('Aparência acima de 4MiB.')
    return dict(pdf=base64.b64encode(raw).decode('ascii'),shaped_unicode=True,clipped_to_rectangle=True)
