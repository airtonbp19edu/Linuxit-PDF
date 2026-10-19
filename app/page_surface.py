"""Paint a bounded raster at logical zoom without allocating a giant pixbuf."""
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk, GObject


class PageViewport(Gtk.Overlay, Gtk.Scrollable):
    """Scroll logical page coordinates while all native windows stay viewport-sized."""
    hadjustment = GObject.Property(type=Gtk.Adjustment)
    vadjustment = GObject.Property(type=Gtk.Adjustment)
    hscroll_policy = GObject.Property(type=Gtk.ScrollablePolicy, default=Gtk.ScrollablePolicy.MINIMUM)
    vscroll_policy = GObject.Property(type=Gtk.ScrollablePolicy, default=Gtk.ScrollablePolicy.MINIMUM)

    def __init__(self):
        super().__init__()
        self.logical_size = (1, 1)
        self._adjustment_signals = []
        self.connect('notify::hadjustment', self._adjustments_changed)
        self.connect('notify::vadjustment', self._adjustments_changed)
        self.connect('size-allocate', lambda *_:self._configure())
        self.props.hadjustment = Gtk.Adjustment()
        self.props.vadjustment = Gtk.Adjustment()

    def _adjustments_changed(self, *_args):
        for adjustment, signal in self._adjustment_signals:adjustment.disconnect(signal)
        self._adjustment_signals = []
        for adjustment in (self.props.hadjustment, self.props.vadjustment):
            if adjustment is not None:
                self._adjustment_signals.append((adjustment, adjustment.connect('value-changed', lambda *_:self.queue_draw())))
        self._configure()

    def _configure(self):
        allocation = self.get_allocation()
        for adjustment, length, available in (
                (self.props.hadjustment, self.logical_size[0], allocation.width),
                (self.props.vadjustment, self.logical_size[1], allocation.height)):
            if adjustment is not None:
                available = max(1, available)
                upper = max(length + 48, available)
                value = max(0, min(adjustment.get_value(), upper - available))
                adjustment.configure(value, 0, upper, 40, available * .9, available)

    def set_page_size(self, width, height):
        self.logical_size = (max(1, width), max(1, height))
        self._configure(); self.queue_draw()

    def page_origin(self):
        allocation = self.get_allocation()
        return (max(24, (allocation.width - self.logical_size[0]) / 2), 24)

    def offset(self):
        x, y = self.page_origin()
        return (x - self.props.hadjustment.get_value(), y - self.props.vadjustment.get_value())

    def page_event(self, event):
        x, y = self.offset()
        class PageEvent:
            def __getattr__(self, name):return getattr(event, name)
        result = PageEvent(); result.x = event.x - x; result.y = event.y - y
        return result


class PageSurface(Gtk.DrawingArea):
    def __init__(self, viewport=None):
        super().__init__()
        self.set_has_window(False)
        self.viewport = viewport
        self.pixbuf = None
        self.display_size = (1, 1)
        self.connect('draw', self._paint)

    def set_from_pixbuf(self, pixbuf, size=None):
        self.pixbuf = pixbuf
        self.display_size = size or (pixbuf.get_width(), pixbuf.get_height())
        if self.viewport is None:self.set_size_request(*self.display_size)
        self.queue_draw()

    def get_pixbuf(self):
        return self.pixbuf

    def clear(self):
        self.pixbuf = None
        self.display_size = (1, 1)
        self.set_size_request(1, 1)
        self.queue_draw()

    def _paint(self, _widget, cr):
        if self.pixbuf is None:return False
        width, height = self.display_size
        cr.save()
        if self.viewport is not None:cr.translate(*self.viewport.offset())
        cr.rectangle(0, 0, width, height); cr.clip()
        cr.scale(width / self.pixbuf.get_width(), height / self.pixbuf.get_height())
        cr.set_source_rgb(1, 1, 1); cr.paint()
        Gdk.cairo_set_source_pixbuf(cr, self.pixbuf, 0, 0)
        cr.paint(); cr.restore()
        return False
