"""Measurements on a bounded snapshot of the currently displayed PDF page."""
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,Gdk
from measurement import measure,calibrated_scale,UNITS_MM,MAX_POINTS


class MeasurementWindow(Gtk.Window):
    def __init__(self,parent,pixbuf,page_size,title):
        super().__init__(title='Medidas — '+title,transient_for=parent)
        self.set_destroy_with_parent(True);self.set_default_size(850,700)
        self.pixbuf=pixbuf;self.page_size=page_size;self.points=[];self.scale=25.4/72
        box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=8,margin=10);self.add(box)
        row=Gtk.Box(spacing=6);box.pack_start(row,False,False,0)
        self.kind=Gtk.ComboBoxText()
        for key,label in [('distance','Distância'),('perimeter','Perímetro fechado'),('area','Área')]:self.kind.append(key,label)
        self.kind.set_active_id('distance');row.add(self.kind)
        self.unit=Gtk.ComboBoxText()
        for unit in UNITS_MM:self.unit.append(unit,unit)
        self.unit.set_active_id('cm');row.add(self.unit)
        done=Gtk.Button(label='Concluir');done.connect('clicked',self._measure);row.add(done)
        clear=Gtk.Button(label='Limpar pontos');clear.connect('clicked',self._clear);row.add(clear)
        hint=Gtk.Label(label='Clique nos pontos da página e conclua. A calibração vale nesta janela; o PDF original é preservado.',xalign=0)
        hint.set_line_wrap(True);box.pack_start(hint,False,False,0)
        self.canvas=Gtk.DrawingArea();self.canvas.set_hexpand(True);self.canvas.set_vexpand(True)
        self.canvas.get_accessible().set_name('Página para posicionar pontos de medição')
        self.canvas.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.canvas.connect('button-press-event',self._click);self.canvas.connect('draw',self._draw)
        box.pack_start(self.canvas,True,True,0)
        row=Gtk.Box(spacing=6);box.pack_start(row,False,False,0)
        row.add(Gtk.Label(label='Comprimento conhecido dos2 primeiros pontos:'))
        self.known=Gtk.SpinButton.new_with_range(.0001,1e9,.1);self.known.set_digits(4);self.known.set_value(1);row.add(self.known)
        calibrate=Gtk.Button(label='Calibrar na unidade selecionada');calibrate.connect('clicked',self._calibrate);row.add(calibrate)
        reset=Gtk.Button(label='Escala PDF');reset.connect('clicked',self._reset_scale);row.add(reset)
        self.status=Gtk.Label(label='Escala inicial:72 pontos por polegada.',xalign=0);self.status.set_line_wrap(True)
        self.status.set_selectable(True);box.pack_start(self.status,False,False,0)

    def _geometry(self):
        pw,ph=self.page_size
        scale=max(.0001,min((self.canvas.get_allocated_width()-20)/pw,(self.canvas.get_allocated_height()-20)/ph))
        return scale,10,10

    def _draw(self,widget,cr):
        scale,x,y=self._geometry();pw,ph=self.page_size
        cr.set_source_rgb(.8,.8,.8);cr.paint();cr.save();cr.translate(x,y)
        cr.scale(pw*scale/self.pixbuf.get_width(),ph*scale/self.pixbuf.get_height())
        Gdk.cairo_set_source_pixbuf(cr,self.pixbuf,0,0);cr.paint();cr.restore()
        cr.set_source_rgb(1,0,0);cr.set_line_width(2)
        for i,(px,py) in enumerate(self.points):
            if i:cr.line_to(x+px*scale,y+py*scale)
            else:cr.move_to(x+px*scale,y+py*scale)
        if len(self.points)>2 and self.kind.get_active_id() in ('perimeter','area'):cr.close_path()
        cr.stroke()
        for px,py in self.points:
            cr.arc(x+px*scale,y+py*scale,3,0,6.283185);cr.fill()
        return False

    def _click(self,widget,event):
        if event.button!=1:return False
        scale,x,y=self._geometry();point=((event.x-x)/scale,(event.y-y)/scale)
        if 0<=point[0]<=self.page_size[0] and 0<=point[1]<=self.page_size[1] and len(self.points)<MAX_POINTS:
            self.points.append(point);self.status.set_text(f'{len(self.points)} ponto(s).');self.canvas.queue_draw()
        return True

    def _measure(self,*_):
        try:
            kind=self.kind.get_active_id();unit=self.unit.get_active_id()
            result=measure(self.points,kind,unit,self.scale)
            self.status.set_text(f'{result:.6g} {unit}'+('²' if kind=='area' else ''))
        except ValueError as exc:self.status.set_text(str(exc))

    def _calibrate(self,*_):
        try:
            self.scale=calibrated_scale(self.points[:2],self.known.get_value(),self.unit.get_active_id())
            self.status.set_text('Escala calibrada. Limpe os pontos para a próxima medida.')
        except ValueError as exc:self.status.set_text(str(exc))

    def _reset_scale(self,*_):self.scale=25.4/72;self.status.set_text('Escala PDF restaurada.')
    def _clear(self,*_):self.points=[];self.canvas.queue_draw();self.status.set_text('Pontos removidos; escala preservada.')
