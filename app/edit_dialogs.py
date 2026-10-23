"""GTK operation choices for the explicit copy-edit draft."""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
from attachment_tasks import display_attachment_name


def ink_operation_dialog(parent, info, page):
    """A bounded page-shaped drawing pad; original PDF remains untouched."""
    from pdf_annotations import create_ink
    dialog=Gtk.Dialog(title='Desenhar à mão livre',transient_for=parent,modal=True)
    dialog.set_destroy_with_parent(True)
    dialog.add_buttons('Cancelar',Gtk.ResponseType.CANCEL,'Preparar desenho',Gtk.ResponseType.OK)
    box=dialog.get_content_area();box.set_spacing(6);box.set_border_width(10)
    hint=Gtk.Label(label='Desenhe na folha abaixo. Ela representa a página antes da rotação, sem o conteúdo de fundo.',xalign=0)
    hint.set_line_wrap(True);box.add(hint)
    area=Gtk.DrawingArea();area.set_size_request(480,400)
    area.get_accessible().set_name('Folha para desenhar à mão livre')
    area.add_events(Gdk.EventMask.BUTTON_PRESS_MASK|Gdk.EventMask.BUTTON_RELEASE_MASK|Gdk.EventMask.POINTER_MOTION_MASK)
    box.add(area);paths=[];state={'active':False}
    left,bottom,right,top=info['page_boxes'][page];width,height=right-left,top-bottom
    def geometry():
        scale=min((area.get_allocated_width()-20)/width,(area.get_allocated_height()-20)/height)
        return max(.0001,scale)
    def point(event):
        scale=geometry();x=left+(event.x-10)/scale;y=top-(event.y-10)/scale
        return (x,y) if left<=x<=right and bottom<=y<=top else None
    def draw(widget,cr):
        cr.set_source_rgb(.85,.85,.85);cr.paint();scale=geometry()
        cr.set_source_rgb(1,1,1);cr.rectangle(10,10,width*scale,height*scale);cr.fill()
        cr.set_source_rgb(1,0,0);cr.set_line_width(1.5)
        for path in paths:
            if len(path)<2:continue
            cr.move_to(10+(path[0]-left)*scale,10+(top-path[1])*scale)
            for x,y in zip(path[2::2],path[3::2]):cr.line_to(10+(x-left)*scale,10+(top-y)*scale)
            cr.stroke()
        return False
    def press(widget,event):
        position=point(event)
        if event.button==1 and position and len(paths)<32:
            paths.append(list(position));state['active']=True;area.queue_draw()
        return True
    def motion(widget,event):
        position=point(event)
        if state['active'] and position and sum(len(p)//2 for p in paths)<4096:
            paths[-1].extend(position);area.queue_draw()
        return True
    def release(widget,event):
        if event.button==1:
            if state['active']:motion(widget,event)
            state['active']=False
            if paths and len(paths[-1])<4:paths.pop()
        return True
    area.connect('draw',draw);area.connect('button-press-event',press)
    area.connect('motion-notify-event',motion);area.connect('button-release-event',release)
    clear=Gtk.Button(label='Limpar desenho')
    def clear_paths(*_):paths.clear();state['active']=False;area.queue_draw()
    clear.connect('clicked',clear_paths);box.add(clear)
    text=Gtk.Entry();text.set_placeholder_text('Comentário opcional');box.add(text)
    error=Gtk.Label(xalign=0);error.set_line_wrap(True);box.add(error);dialog.show_all()
    try:
        while dialog.run()==Gtk.ResponseType.OK:
            try:
                create_ink(info['page_boxes'][page],paths,text.get_text())
                return dict(kind='add-ink',page=page,paths=paths,text=text.get_text())
            except ValueError as exc:error.set_text(str(exc))
        return None
    finally:dialog.destroy()

ADVANCED_KINDS = {'move-bookmark', 'delete-bookmark', 'fill-form-controls', 'fill-form-events', 'fill-form-javascript',
                  'delete-annotation', 'update-annotation', 'add-highlight', 'add-rectangle',
                  'add-underline', 'add-strikeout', 'add-squiggly', 'add-ellipse', 'add-line', 'add-ink', 'add-reply'}
ADVANCED_KINDS.update({'style-annotation','resize-annotation','add-redaction'})
ADVANCED_KINDS.update({'add-polygon','add-polyline','add-caret','add-freetext','add-stamp',
                       'move-annotation','update-comment','set-popup','delete-conversation'})
TITLES = {'move-bookmark':'Mover marcador', 'delete-bookmark':'Excluir marcador e descendentes',
          'fill-form-controls':'Preencher caixas e listas', 'delete-annotation':'Excluir anotação',
          'add-highlight':'Destacar área', 'add-rectangle':'Adicionar retângulo',
          'add-underline':'Sublinhar área', 'add-strikeout':'Tachar área', 'add-squiggly':'Sublinhar área com ondulado',
          'add-ellipse':'Adicionar elipse', 'add-line':'Adicionar linha', 'update-annotation':'Editar comentário da anotação'}
TITLES.update({'add-ink':'Desenhar à mão livre','add-reply':'Responder comentário'})
TITLES['fill-form-events']='Preencher com cálculos e validação'
TITLES['fill-form-javascript']='Preencher com JavaScript isolado'
TITLES['style-annotation']='Cor e opacidade da anotação'
TITLES['resize-annotation']='Redimensionar anotação'
TITLES['add-redaction']='Marcar área para redação'
TITLES.update({'add-polygon':'Adicionar polígono','add-polyline':'Adicionar polilinha','add-caret':'Marcar inserção',
    'add-freetext':'Adicionar texto livre','add-stamp':'Adicionar carimbo textual','move-annotation':'Mover anotação',
    'update-comment':'Editar comentário ou resposta','set-popup':'Configurar popup','delete-conversation':'Excluir conversa e popups'})


def advanced_operation_dialog(parent, kind, info, page):
    if kind == 'add-ink':return ink_operation_dialog(parent,info,page)
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
    elif kind in ('add-polygon','add-polyline'):
        combo.set_no_show_all(True);combo.hide()
        hint.set_text('Informe um vértice por linha como X,Y em pontos PDF antes da rotação. Máximo 512; polígono exige ao menos 3 sem cruzamento.')
        vertices=Gtk.TextView();vertices.set_wrap_mode(Gtk.WrapMode.NONE);vertices.get_accessible().set_name('Vértices X,Y')
        left,bottom,right,top=info['page_boxes'][page];w,h=right-left,top-bottom
        vertices.get_buffer().set_text(f'{left+w*.1},{bottom+h*.1}\n{left+w*.5},{bottom+h*.7}\n{left+w*.8},{bottom+h*.1}')
        scroll=Gtk.ScrolledWindow();scroll.set_min_content_height(140);scroll.add(vertices);box.add(scroll)
        comment=Gtk.Entry();comment.set_placeholder_text('Comentário opcional');box.add(comment)
        def operation():
            buffer=vertices.get_buffer();raw=buffer.get_text(buffer.get_start_iter(),buffer.get_end_iter(),True)
            try:coords=[[float(v.strip()) for v in line.split(',')] for line in raw.splitlines() if line.strip()]
            except ValueError as exc:raise ValueError('Use X,Y numéricos por linha.') from exc
            return dict(kind=kind,page=page,points=coords,text=comment.get_text())
    elif kind in ('move-annotation','update-comment','delete-conversation','set-popup'):
        records=[r for r in info.get('annotations' if kind=='move-annotation' else 'conversation_comments',[]) if r['page']==page]
        for record in records:combo.append_text(f"{record['index']+1} · {display_attachment_name(record['text'][:80])}")
        if kind=='move-annotation':
            hint.set_text('Move uma anotação simples sem respostas/popup. Deslocamentos em pontos PDF; a forma inteira deve ficar na página.')
            width=info['page_boxes'][page][2]-info['page_boxes'][page][0];height=info['page_boxes'][page][3]-info['page_boxes'][page][1]
            dx=Gtk.SpinButton.new_with_range(-width,width,.5);dy=Gtk.SpinButton.new_with_range(-height,height,.5)
            box.add(Gtk.Label(label='Deslocamento horizontal'));box.add(dx);box.add(Gtk.Label(label='Deslocamento vertical'));box.add(dy)
        elif kind=='update-comment':
            comment=Gtk.TextView();comment.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
            scroll=Gtk.ScrolledWindow();scroll.set_min_content_height(120);scroll.add(comment);box.add(scroll)
            author=Gtk.Entry();author.set_placeholder_text('Autor opcional');box.add(author)
            def selected(*_):
                if combo.get_active()>=0:
                    record=records[combo.get_active()];comment.get_buffer().set_text(record['text']);author.set_text(record.get('author',''))
            combo.connect('changed',selected)
            hint.set_text('Edita o comentário ou resposta, conservando vínculos. Texto livre/carimbo recebem aparência atualizada na cópia.')
        elif kind=='set-popup':
            left,bottom,right,top=info['page_boxes'][page];w,h=right-left,top-bottom
            spins=[]
            for label,low,high,value in [('Esquerda',left,right,left+w*.5),('Inferior',bottom,top,bottom+h*.5),('Direita',left,right,right-w*.05),('Superior',bottom,top,top-h*.05)]:
                spin=Gtk.SpinButton.new_with_range(low,high,.5);spin.set_value(value);box.add(Gtk.Label(label=label));box.add(spin);spins.append(spin)
            opened=Gtk.CheckButton(label='Abrir popup ao visualizar');opened.set_active(True);box.add(opened)
        else:hint.set_text('Exclui este comentário, suas respostas e popups da cópia. Objetos bloqueados e vínculos entre páginas impedem a operação.')
        def operation():
            if combo.get_active()<0:raise ValueError('Nenhum comentário compatível nesta página.')
            result=dict(kind=kind,page=page,index=records[combo.get_active()]['index'])
            if kind=='move-annotation':result.update(dx=dx.get_value(),dy=dy.get_value())
            elif kind=='update-comment':
                buffer=comment.get_buffer();result.update(text=buffer.get_text(buffer.get_start_iter(),buffer.get_end_iter(),True),author=author.get_text())
            elif kind=='set-popup':result.update(rect=[s.get_value() for s in spins],open=opened.get_active())
            return result
    elif kind in ('fill-form-events', 'fill-form-javascript'):
        configuration=info.get('form_events',{})
        calculated={r['field'] for r in configuration.get('rules',[]) if r['event']=='/C'}
        if kind == 'fill-form-events' and configuration.get('unsupported'):
            dialog.destroy();raise ValueError('Este formulário contém eventos fora do subconjunto suportado. Nenhum script foi executado.')
        if kind == 'fill-form-javascript':
            from pdf_form_javascript import available
            if not available():
                dialog.destroy();raise ValueError('JavaScript isolado requer python-quickjs-ng 0.15.1.1.')
            calculated.update(r['field'] for r in configuration.get('unsupported',[]) if r['event']=='/C')
        records=[r for r in info['text_fields'] if not r['read_only'] and r['name'] not in calculated]
        if not records:
            dialog.destroy();raise ValueError('Nenhum campo de entrada editável disponível.')
        hint.set_text('Preencha entradas. Cálculos simples e limites numéricos reconhecidos serão aplicados à cópia; scripts gerais não são executados.')
        if kind == 'fill-form-javascript':
            hint.set_text('Ao confirmar você autoriza os eventos K/V/C/F em um processo QuickJS limitado, sem rede nem arquivos. Ações ao abrir, scripts de documento e APIs externas não são executados. Erros cancelam a cópia inteira.')
        fields=[];grid=Gtk.Grid(column_spacing=8,row_spacing=6)
        for row,record in enumerate(records[:256]):
            entry=Gtk.Entry();entry.set_text(record['value']);entry.get_accessible().set_name(record['name'])
            label=Gtk.Label(label=record['name'],xalign=0);grid.attach(label,0,row,1,1);grid.attach(entry,1,row,1,1)
            fields.append((record,entry))
        scroll=Gtk.ScrolledWindow();scroll.set_min_content_height(180);scroll.set_max_content_height(400)
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC,Gtk.PolicyType.AUTOMATIC);scroll.add(grid);box.pack_start(scroll,True,True,0)
        def operation():
            return dict(kind=kind,values={r['name']:entry.get_text() for r,entry in fields})
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
            elif record.get('editable'):
                widget = Gtk.ComboBoxText.new_with_entry()
                for option in record['options']:widget.append_text(option['label'])
                exports = [o['value'] for o in record['options']]
                value = record['value'][0] if record['value'] else ''
                if value in exports:widget.set_active(exports.index(value))
                else:widget.get_child().set_text(value)
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
            elif record.get('editable'):
                selected = widget.get_active()
                text = widget.get_child().get_text()
                value = [record['options'][selected]['value'] if selected >= 0 else text] if text else []
            else:value = [] if widget.get_active() == 0 else [record['options'][widget.get_active()-1]['value']]
            return {'kind':kind, 'values':{record['name']:value}}
    elif kind == 'add-reply':
        records=[r for r in info.get('reply_targets',[]) if r['page']==page]
        for record in records:combo.append_text(f"{record['index']+1} · {display_attachment_name(record['text'])}")
        comment=Gtk.TextView();comment.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        comment.get_accessible().set_name('Texto da resposta')
        scroll=Gtk.ScrolledWindow();scroll.set_min_content_height(120);scroll.add(comment);box.add(scroll)
        author=Gtk.Entry();author.set_placeholder_text('Autor da resposta');box.add(author)
        hint.set_text('Selecione o comentário desta página. A resposta será adicionada à conversa na cópia.')
        def operation():
            if combo.get_active()<0:raise ValueError('Não há comentários de destino suportados.')
            buffer=comment.get_buffer();text=buffer.get_text(buffer.get_start_iter(),buffer.get_end_iter(),True)
            if not text.strip():raise ValueError('Digite a resposta.')
            return dict(kind=kind,page=page,index=records[combo.get_active()]['index'],text=text,author=author.get_text())
    elif kind == 'resize-annotation':
        # E13: new rectangle for rectangles, ellipses and free text, appearance regenerated.
        records = [r for r in info.get('annotations', []) if r['page'] == page and r.get('resizable') and r.get('rect')]
        names = {'/Square':'Retângulo','/Circle':'Elipse','/FreeText':'Texto livre','/Redact':'Redação marcada'}
        for record in records:combo.append_text(f"{names.get(record['subtype'],record['subtype'])} {record['index']+1} · {display_attachment_name(record['text'][:80])}")
        left, bottom, right, top = info['page_boxes'][page]
        grid = Gtk.Grid(column_spacing=10, row_spacing=6);box.add(grid);spins = []
        for row, label in enumerate(('Esquerda', 'Inferior', 'Direita', 'Superior')):
            low, high = (left, right) if row in (0, 2) else (bottom, top)
            spin = Gtk.SpinButton.new_with_range(low, high, 1);spin.set_digits(1);spin.get_accessible().set_name(label)
            grid.attach(Gtk.Label(label=label, xalign=0), 0, row, 1, 1);grid.attach(spin, 1, row, 1, 1);spins.append(spin)
        def selected_rect(*_):
            if combo.get_active() < 0:return
            for spin, value in zip(spins, records[combo.get_active()]['rect']):spin.set_value(value)
        combo.connect('changed', selected_rect)
        hint.set_text('Informe a nova área em pontos PDF, antes da rotação. O desenho é refeito no novo tamanho; o texto livre é diagramado de novo.')
        def operation():
            if combo.get_active() < 0:raise ValueError('Não há retângulos, elipses ou textos livres nesta página.')
            return dict(kind=kind, page=page, index=records[combo.get_active()]['index'], rect=[round(s.get_value(), 3) for s in spins])
    elif kind == 'style-annotation':
        # E12: colour and opacity of existing simple annotations; appearance regenerated.
        records = [r for r in info.get('annotations', []) if r['page'] == page and r.get('styleable')]
        names = {'/Square':'Retângulo','/Highlight':'Destaque','/Underline':'Sublinhado','/StrikeOut':'Tachado',
                 '/Squiggly':'Ondulado','/Circle':'Elipse','/Line':'Linha','/Ink':'Desenho','/Polygon':'Polígono',
                 '/PolyLine':'Polilinha','/Caret':'Inserção'}
        for record in records:combo.append_text(f"{names.get(record['subtype'],record['subtype'])} {record['index']+1} · {display_attachment_name(record['text'][:80])}")
        color_button = Gtk.ColorButton();color_button.set_use_alpha(False);color_button.get_accessible().set_name('Cor da anotação')
        opacity = Gtk.SpinButton.new_with_range(10, 100, 5);opacity.set_value(100);opacity.get_accessible().set_name('Opacidade em porcentagem')
        grid = Gtk.Grid(column_spacing=10, row_spacing=6);box.add(grid)
        grid.attach(Gtk.Label(label='Cor', xalign=0), 0, 0, 1, 1);grid.attach(color_button, 1, 0, 1, 1)
        grid.attach(Gtk.Label(label='Opacidade (%)', xalign=0), 0, 1, 1, 1);grid.attach(opacity, 1, 1, 1, 1)
        def selected_style(*_):
            if combo.get_active() < 0:return
            record = records[combo.get_active()];rgba = Gdk.RGBA()
            rgba.red, rgba.green, rgba.blue = record.get('color') or (1, 0, 0);rgba.alpha = 1
            color_button.set_rgba(rgba);opacity.set_value(round(100 * record.get('opacity', 1)))
        combo.connect('changed', selected_style)
        hint.set_text('Muda cor e opacidade de retângulos, elipses, linhas, destaques, sublinhados, desenhos e polígonos já existentes; a aparência é redesenhada a partir da geometria. Notas, texto livre e carimbos não entram.')
        def operation():
            if combo.get_active() < 0:raise ValueError('Não há anotações com cor editável nesta página.')
            rgba = color_button.get_rgba()
            return dict(kind=kind, page=page, index=records[combo.get_active()]['index'],
                        color=[round(rgba.red, 4), round(rgba.green, 4), round(rgba.blue, 4)],
                        opacity=round(opacity.get_value() / 100, 4))
    elif kind in ('delete-annotation','update-annotation'):
        records = [r for r in info.get('annotations', []) if r['page'] == page]
        names = {'/Text':'Nota','/Square':'Retângulo','/Highlight':'Destaque','/Underline':'Sublinhado',
                 '/StrikeOut':'Tachado','/Squiggly':'Ondulado','/Circle':'Elipse','/Line':'Linha','/Ink':'Desenho',
                 '/Redact':'Redação marcada'}
        for record in records:combo.append_text(f"{names.get(record['subtype'],record['subtype'])} {record['index']+1} · {display_attachment_name(record['text'][:80])}")
        if kind == 'update-annotation':
            box.add(Gtk.Label(label='Comentário (pode ficar vazio)', xalign=0))
            comment = Gtk.TextView();comment.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
            comment.get_accessible().set_name('Comentário da anotação')
            scroll = Gtk.ScrolledWindow();scroll.set_min_content_height(100);scroll.add(comment);box.add(scroll)
            author = Gtk.Entry();author.get_accessible().set_name('Autor da anotação');author.set_placeholder_text('Autor opcional');box.add(author)
            def selected_annotation(*_):
                if combo.get_active() < 0:return
                record = records[combo.get_active()]
                comment.get_buffer().set_text(record['text']);author.set_text(record.get('author', ''))
            combo.connect('changed', selected_annotation)
            hint.set_text('Edite comentário e autor. A posição e a aparência da anotação serão preservadas. Anotações com bloqueios, respostas ou popup são recusadas.')
        def operation():
            if combo.get_active() < 0:raise ValueError('Não há anotações editáveis suportadas nesta página.')
            result = {'kind':kind, 'page':page, 'index':records[combo.get_active()]['index']}
            if kind == 'update-annotation':
                buffer = comment.get_buffer()
                result.update(text=buffer.get_text(buffer.get_start_iter(),buffer.get_end_iter(),True),author=author.get_text())
            return result
    else:
        combo.set_no_show_all(True);combo.hide()
        left, bottom, right, top = info['page_boxes'][page]
        hint.set_text('Informe os limites em pontos PDF, antes da rotação da página. A área deve ficar dentro da página.')
        grid = Gtk.Grid(column_spacing=10, row_spacing=6);box.add(grid);spins = []
        width, height = right-left, top-bottom
        line = kind == 'add-line'
        if line:hint.set_text('Informe início e fim em pontos PDF, antes da rotação. A linha pode ser horizontal, vertical ou diagonal; deve ficar dentro da página. Sem pontas de seta.')
        elif kind in ('add-freetext','add-stamp'):
            hint.set_text('Texto Unicode com fontes incorporadas na aparência. A área limita o texto visível; aumente-a para acomodar todo o conteúdo.')
        elif kind == 'add-redaction':
            hint.set_text('Marca a área com contorno tracejado vermelho, sem apagar nada. A marca pode ser movida, redimensionada, comentada ou excluída; o conteúdo só é removido ao aplicar a redação, em uma cópia nova.')
        elif kind not in ('add-highlight','add-rectangle'):
            hint.set_text(hint.get_text()+' Traço vermelho. A área é manual; não seleciona palavras automaticamente.')
        bounds = ((('X inicial' if line else 'Esquerda'),left,right,left+width*.1),
                  (('Y inicial' if line else 'Inferior'),bottom,top,bottom+height*.1),
                  (('X final' if line else 'Direita'),left,right,right-width*.1),
                  (('Y final' if line else 'Superior'),bottom,top,bottom+height*.2))
        for row,(name,low,high,value) in enumerate(bounds):
            spin = Gtk.SpinButton.new_with_range(low,high,.5);spin.set_digits(1);spin.set_value(value)
            spin.get_accessible().set_name(name);spins.append(spin)
            grid.attach(Gtk.Label(label=name,xalign=0),0,row,1,1);grid.attach(spin,1,row,1,1)
        if kind in ('add-freetext','add-stamp'):
            text=Gtk.TextView();text.set_wrap_mode(Gtk.WrapMode.WORD_CHAR);text.get_accessible().set_name('Texto da anotação')
            scroll=Gtk.ScrolledWindow();scroll.set_min_content_height(100);scroll.add(text);box.add(scroll)
        else:
            text = Gtk.Entry();text.get_accessible().set_name('Comentário da anotação');text.set_placeholder_text('Comentário opcional');box.add(text)
        def operation():
            rect = [s.get_value() for s in spins]
            if line:
                if ((rect[2]-rect[0])**2+(rect[3]-rect[1])**2)**.5 < .25:raise ValueError('A linha deve medir ao menos 0,25 ponto.')
            elif not rect[0] < rect[2] or not rect[1] < rect[3]:raise ValueError('Os limites precisam formar uma área com largura e altura positivas.')
            elif kind not in ('add-highlight','add-rectangle') and (rect[2]-rect[0] < .25 or rect[3]-rect[1] < .25):
                raise ValueError('A área deve ter largura e altura de ao menos 0,25 ponto.')
            if isinstance(text,Gtk.TextView):
                buffer=text.get_buffer();contents=buffer.get_text(buffer.get_start_iter(),buffer.get_end_iter(),True)
            else:contents=text.get_text()
            return {'kind':kind,'page':page,('points' if line else 'rect'):rect,'text':contents}
    box.add(error);combo.set_active(0);dialog.show_all()
    try:
        while dialog.run() == Gtk.ResponseType.OK:
            try:return operation()
            except ValueError as exc:error.set_text(str(exc))
        return None
    finally:dialog.destroy()


def redaction_apply_dialog(parent, marks):
    """Confirm the selected redaction method; raster returns its historical DPI value."""
    dialog = Gtk.Dialog(title='Aplicar redação', transient_for=parent, modal=True)
    dialog.add_buttons('Cancelar', Gtk.ResponseType.CANCEL, 'Escolher destino…', Gtk.ResponseType.OK)
    box = dialog.get_content_area();box.set_spacing(8);box.set_border_width(12)
    text = Gtk.Label(label=(f'{marks} área(s) marcada(s). Numa cópia nova, o texto, os desenhos e as imagens sob as áreas são '
                            'removidos e pintados com a cor de preenchimento da marca. No método rasterizado, cada página com marcas vira uma imagem: '
                            'o texto dela deixa de ser selecionável e pesquisável. Anotações sobre as áreas são removidas; '
                            'páginas sem marcas não mudam. Títulos de marcadores, metadados e anexos não são verificados.'), xalign=0)
    text.set_line_wrap(True);text.set_max_width_chars(70);box.add(text)
    method = Gtk.ComboBoxText();method.get_accessible().set_name('Método de redação')
    method.append('raster','Rasterizado (compatibilidade ampla)')
    method.append('vector','Sem rasterizar (objetos simples; formulários gráficos removidos inteiros)');method.set_active_id('raster');box.add(method)
    explanation=Gtk.Label(label='Sem rasterizar: remove objetos inteiros que tocam a área; pode remover texto ou desenho vizinho. Conteúdo complexo é recusado. O texto restante continua selecionável.',xalign=0)
    explanation.set_line_wrap(True);explanation.set_max_width_chars(70);box.add(explanation)
    resolution = Gtk.ComboBoxText();resolution.get_accessible().set_name('Resolução das páginas redigidas')
    resolution.append('150', '150 DPI (arquivo menor)');resolution.append('300', '300 DPI (mais nítido)')
    resolution.set_active_id('150');box.add(resolution)
    method.connect('changed',lambda *_:resolution.set_sensitive(method.get_active_id()=='raster'))
    dialog.show_all()
    try:
        if dialog.run()!=Gtk.ResponseType.OK:return None
        dpi=int(resolution.get_active_id())
        return {'mode':'vector','dpi':dpi} if method.get_active_id()=='vector' else dpi
    finally:dialog.destroy()
