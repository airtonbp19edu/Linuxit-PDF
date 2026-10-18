"""GTK operation choices for the explicit copy-edit draft."""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from attachment_tasks import display_attachment_name

ADVANCED_KINDS = {'move-bookmark', 'delete-bookmark', 'fill-form-controls',
                  'delete-annotation', 'add-highlight', 'add-rectangle'}
TITLES = {'move-bookmark':'Mover marcador', 'delete-bookmark':'Excluir marcador e descendentes',
          'fill-form-controls':'Preencher caixas e listas', 'delete-annotation':'Excluir anotação',
          'add-highlight':'Destacar área', 'add-rectangle':'Adicionar retângulo'}


def advanced_operation_dialog(parent, kind, info, page):
    if kind not in ADVANCED_KINDS:return None
    dialog = Gtk.Dialog(title=TITLES[kind], transient_for=parent, modal=True)
    dialog.set_destroy_with_parent(True)
    dialog.add_buttons('Cancelar', Gtk.ResponseType.CANCEL, 'Preparar alteração', Gtk.ResponseType.OK)
    dialog.set_default_size(500, -1)
    box = dialog.get_content_area();box.set_spacing(8);box.set_border_width(12)
    hint = Gtk.Label(label='A alteração será aplicada ao rascunho de uma cópia nova.', xalign=0)
    hint.set_line_wrap(True);box.add(hint)
    error = Gtk.Label(xalign=0);error.set_line_wrap(True)
    combo = Gtk.ComboBoxText();combo.get_accessible().set_name('Item a alterar')
    box.add(combo)
    if kind in ('move-bookmark','delete-bookmark'):
        records = info.get('bookmarks', [])
        for record in records:
            combo.append_text('/'.join(str(i+1) for i in record['path'])+' · '+display_attachment_name(record['title']))
        if kind == 'move-bookmark':
            box.add(Gtk.Label(label='Novo pai do marcador', xalign=0))
            parents = Gtk.ComboBoxText();parents.get_accessible().set_name('Novo pai do marcador');box.add(parents)
            box.add(Gtk.Label(label='Posição entre os filhos, depois de retirar da origem (1 = primeiro)', xalign=0))
            position = Gtk.SpinButton.new_with_range(1, 2049, 1)
            position.get_accessible().set_name('Nova posição do marcador');box.add(position)
            choices = []
            def target_changed(*_):
                if combo.get_active() < 0 or parents.get_active() < 0:return
                source = records[combo.get_active()]['path'];target = choices[parents.get_active()]
                count = sum(r['path'][:-1] == target and r['path'] != source for r in records)
                position.set_range(1, count+1);position.set_value(count+1)
            def selected_changed(*_):
                parents.remove_all();choices.clear()
                if combo.get_active() < 0:return
                source = records[combo.get_active()]['path']
                choices.append([]);parents.append_text('Nível principal')
                for record in records:
                    if record['path'][:len(source)] == source:continue
                    choices.append(record['path']);parents.append_text('/'.join(str(i+1) for i in record['path'])+' · '+display_attachment_name(record['title']))
                parents.set_active(0)
            combo.connect('changed', selected_changed);parents.connect('changed', target_changed)
        def operation():
            if combo.get_active() < 0:raise ValueError('Não há marcadores disponíveis.')
            result = {'kind':kind,'path':records[combo.get_active()]['path']}
            if kind == 'move-bookmark':result.update(parent=choices[parents.get_active()],position=position.get_value_as_int()-1)
            return result
    elif kind == 'fill-form-controls':
        records = [r for r in info.get('form_controls', []) if not r['read_only']]
        for record in records:combo.append_text(display_attachment_name(record['name']))
        area = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6);box.add(area)
        current = {}
        def changed(*_):
            for child in area.get_children():area.remove(child);child.destroy()
            current.clear()
            if combo.get_active() < 0:return
            record = records[combo.get_active()]
            if record['kind'] == 'checkbox':
                widget = Gtk.CheckButton(label='Marcado');widget.set_active(record['value'])
            elif record['kind'] == 'radio':
                widget = Gtk.ComboBoxText();values = (['/Off'] if record['allow_off'] else []) + record['options']
                for value in values:widget.append_text('Nenhuma opção' if value == '/Off' else display_attachment_name(value[1:]))
                widget.set_active(values.index(record['value']) if record['value'] in values else -1)
                current['values'] = values
            elif record['multiple']:
                widget = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
                checks = []
                for option in record['options']:
                    check = Gtk.CheckButton(label=display_attachment_name(option['label']))
                    check.set_active(option['value'] in record['value']);widget.add(check);checks.append(check)
                current['checks'] = checks
            else:
                widget = Gtk.ComboBoxText();widget.append_text('Sem seleção')
                for option in record['options']:widget.append_text(display_attachment_name(option['label']))
                values = [o['value'] for o in record['options']]
                widget.set_active(values.index(record['value'][0])+1 if record['value'] else 0)
            widget.get_accessible().set_name('Novo valor do controle')
            current['widget'] = widget
            scroll = Gtk.ScrolledWindow();scroll.set_min_content_height(100);scroll.set_max_content_height(240)
            scroll.add(widget);area.add(scroll);area.show_all()
        combo.connect('changed', changed)
        if info.get('unsupported_controls'):
            hint.set_text(hint.get_text()+' Alguns controles não são suportados e foram omitidos.')
        def operation():
            if combo.get_active() < 0:raise ValueError('Não há caixas ou listas editáveis suportadas.')
            record, widget = records[combo.get_active()], current['widget']
            if record['kind'] == 'checkbox':value = widget.get_active()
            elif record['kind'] == 'radio':
                if widget.get_active() < 0:raise ValueError('Selecione uma opção.')
                value = current['values'][widget.get_active()]
            elif record['multiple']:value = [o['value'] for o,c in zip(record['options'], current['checks']) if c.get_active()]
            else:value = [] if widget.get_active() == 0 else [record['options'][widget.get_active()-1]['value']]
            return {'kind':kind, 'values':{record['name']:value}}
    elif kind == 'delete-annotation':
        records = [r for r in info.get('annotations', []) if r['page'] == page]
        names = {'/Text':'Nota','/Square':'Retângulo','/Highlight':'Destaque'}
        for record in records:combo.append_text(f"{names[record['subtype']]} {record['index']+1} · {display_attachment_name(record['text'][:80])}")
        def operation():
            if combo.get_active() < 0:raise ValueError('Não há anotações editáveis suportadas nesta página.')
            return {'kind':kind, 'page':page, 'index':records[combo.get_active()]['index']}
    else:
        combo.set_no_show_all(True);combo.hide()
        left, bottom, right, top = info['page_boxes'][page]
        hint.set_text('Informe os limites em pontos PDF, antes da rotação da página. A área deve ficar dentro da página.')
        grid = Gtk.Grid(column_spacing=10, row_spacing=6);box.add(grid);spins = []
        width, height = right-left, top-bottom
        for row,(name,low,high,value) in enumerate((('Esquerda',left,right,left+width*.1),('Inferior',bottom,top,bottom+height*.1),
                                                  ('Direita',left,right,right-width*.1),('Superior',bottom,top,bottom+height*.2))):
            spin = Gtk.SpinButton.new_with_range(low,high,.5);spin.set_digits(1);spin.set_value(value)
            spin.get_accessible().set_name(name);spins.append(spin)
            grid.attach(Gtk.Label(label=name,xalign=0),0,row,1,1);grid.attach(spin,1,row,1,1)
        text = Gtk.Entry();text.get_accessible().set_name('Comentário da anotação');text.set_placeholder_text('Comentário opcional');box.add(text)
        def operation():
            rect = [s.get_value() for s in spins]
            if not rect[0] < rect[2] or not rect[1] < rect[3]:raise ValueError('Os limites precisam formar uma área com largura e altura positivas.')
            return {'kind':kind,'page':page,'rect':rect,'text':text.get_text()}
    box.add(error);combo.set_active(0);dialog.show_all()
    try:
        while dialog.run() == Gtk.ResponseType.OK:
            try:return operation()
            except ValueError as exc:error.set_text(str(exc))
        return None
    finally:dialog.destroy()
