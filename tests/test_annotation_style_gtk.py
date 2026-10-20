"""E12: the colour/opacity dialog lists only styleable annotations and returns the chosen style."""
import os,sys,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];APP=Path(os.environ.get('PRINT_VIEW_TEST_APP',ROOT/'app'));sys.path.insert(0,str(APP))


@unittest.skipUnless(os.environ.get('DISPLAY'),'Requires GTK3 and a display')
class AnnotationStyleDialogTests(unittest.TestCase):
    def test_dialog_offers_styleable_records_with_current_style_and_returns_operation(self):
        import gi
        gi.require_version('Gtk','3.0');gi.require_version('Gdk','3.0')
        from gi.repository import Gdk,Gtk
        from edit_dialogs import advanced_operation_dialog
        info={'page_boxes':[[0,0,300,300]],'annotations':[
            {'page':0,'index':0,'subtype':'/Text','text':'nota','author':'','styleable':False,'color':None,'opacity':1.0},
            {'page':0,'index':1,'subtype':'/Square','text':'caixa','author':'','styleable':True,'color':[1.0,0.0,0.0],'opacity':0.8}]}
        seen={}
        def run(dialog):
            widgets=[];stack=[dialog]
            while stack:
                widget=stack.pop();widgets.append(widget)
                if isinstance(widget,Gtk.Container):stack.extend(widget.get_children())
            combo=next(w for w in widgets if isinstance(w,Gtk.ComboBoxText))
            seen['items']=[row[0] for row in combo.get_model()]
            button=next(w for w in widgets if isinstance(w,Gtk.ColorButton));spin=next(w for w in widgets if isinstance(w,Gtk.SpinButton))
            seen['initial']=(round(button.get_rgba().red,2),spin.get_value())
            rgba=Gdk.RGBA();rgba.red,rgba.green,rgba.blue,rgba.alpha=0,0,1,1;button.set_rgba(rgba);spin.set_value(50)
            return Gtk.ResponseType.OK
        with patch.object(Gtk.Dialog,'run',run):
            operation=advanced_operation_dialog(None,'style-annotation',info,0)
        self.assertEqual(len(seen['items']),1);self.assertIn('Retângulo 2',seen['items'][0])
        self.assertEqual(seen['initial'],(1.0,80.0))
        self.assertEqual(operation,{'kind':'style-annotation','page':0,'index':1,'color':[0.0,0.0,1.0],'opacity':0.5})

    def test_resize_dialog_prefills_the_current_rectangle_and_returns_the_new_one(self):
        import gi
        gi.require_version('Gtk','3.0')
        from gi.repository import Gtk
        from edit_dialogs import advanced_operation_dialog
        info={'page_boxes':[[0,0,300,300]],'annotations':[
            {'page':0,'index':0,'subtype':'/Line','text':'l','author':'','styleable':True,'resizable':False,'rect':[1,1,9,9],'color':None,'opacity':1.0},
            {'page':0,'index':1,'subtype':'/FreeText','text':'t','author':'','styleable':False,'resizable':True,'rect':[20,20,140,60],'color':None,'opacity':1.0}]}
        seen={}
        def run(dialog):
            widgets=[];stack=[dialog]
            while stack:
                widget=stack.pop();widgets.append(widget)
                if isinstance(widget,Gtk.Container):stack.extend(widget.get_children())
            combo=next(w for w in widgets if isinstance(w,Gtk.ComboBoxText))
            seen['items']=[row[0] for row in combo.get_model()]
            spins={w.get_accessible().get_name():w for w in widgets if isinstance(w,Gtk.SpinButton)}
            seen['initial']=[spins[k].get_value() for k in ('Esquerda','Inferior','Direita','Superior')]
            spins['Direita'].set_value(280)
            return Gtk.ResponseType.OK
        with patch.object(Gtk.Dialog,'run',run):
            operation=advanced_operation_dialog(None,'resize-annotation',info,0)
        self.assertEqual(len(seen['items']),1);self.assertIn('Texto livre 2',seen['items'][0])
        self.assertEqual(seen['initial'],[20,20,140,60])
        self.assertEqual(operation,{'kind':'resize-annotation','page':0,'index':1,'rect':[20,20,280,60]})


if __name__=='__main__':unittest.main()
