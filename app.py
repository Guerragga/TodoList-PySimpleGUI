import PySimpleGUI as sg

# Função para criar a janela principal
def Criar_janela_inicial():
    sg.theme('DarkBlue4')
    
    # Linha de exemplo
    linha_exemplo = [
        sg.Checkbox('', key='-CHECK-0'),
        sg.Input('Tarefa Exemplo', key='-TAREFA-0', size=(30, 1), disabled=True),
        sg.Button('Editar', key='-EDIT-0', size=(8, 1)),
        sg.Button('Excluir', key='-EXCLUIR-0', size=(8, 1))
    ]
    
    layout = [
        [sg.Text('Tarefas')],
        [sg.Column([linha_exemplo], key='container')],
        [sg.Button('Nova Tarefa'), sg.Button('Resetar')]
    ]
    
    return sg.Window('Todo List', layout=layout, finalize=True)

# Função para criar uma nova linha de tarefa com chaves únicas
def Criar_linha_tarefa(num_tarefa, tarefa=''):
    return [
        sg.Checkbox('', key=f'-CHECK-{num_tarefa}'),
        sg.Input(tarefa, key=f'-TAREFA-{num_tarefa}', size=(30, 1), disabled=True),
        sg.Button('Editar', key=f'-EDIT-{num_tarefa}', size=(8, 1)),
        sg.Button('Excluir', key=f'-EXCLUIR-{num_tarefa}', size=(8, 1))
    ]

# Função para habilitar a edição de uma tarefa
def Habilitar_edicao(num_tarefa):
    janela[f'-TAREFA-{num_tarefa}'].update(disabled=False)
    janela[f'-EDIT-{num_tarefa}'].update('Concluir')
    janela[f'-TAREFA-{num_tarefa}'].set_focus()

# Função para concluir a edição de uma tarefa
def Concluir_edicao(num_tarefa):
    janela[f'-TAREFA-{num_tarefa}'].update(disabled=True)
    janela[f'-EDIT-{num_tarefa}'].update('Editar')
    return janela[f'-TAREFA-{num_tarefa}'].get()  # Retorna o valor da tarefa concluída

# Criar a janela
janela = Criar_janela_inicial()
contador_tarefas = 1  # Contador começa em 1 porque já existe uma tarefa (a de exemplo)
tarefa_editando = None  # Variável para rastrear qual tarefa está sendo editada

# Dicionário para armazenar tarefas e seus valores
tarefas = {}

# Gerenciar eventos e valores
while True:
    event, values = janela.read()
    
    if event == sg.WIN_CLOSED:
        break
    
    elif event == 'Nova Tarefa':
        # Incrementa o contador de tarefas para garantir chaves únicas
        contador_tarefas += 1
        # Adiciona uma nova linha de tarefa com um campo habilitado para edição imediata
        janela.extend_layout(janela['container'], [Criar_linha_tarefa(contador_tarefas)])
        key_tarefa = f'-TAREFA-{contador_tarefas}'
        Habilitar_edicao(contador_tarefas)
        tarefa_editando = contador_tarefas
    
    elif event == 'Resetar':
        # Fecha a janela atual e cria uma nova (reseta)
        janela.close()
        janela = Criar_janela_inicial()
        contador_tarefas = 1  # Reseta o contador de tarefas
        tarefa_editando = None  # Reseta a tarefa em edição
        tarefas = {}  # Limpa o dicionário de tarefas
    
    elif event.startswith('-EDIT-'):
        num_tarefa = event.split('-')[2]
        if tarefa_editando and tarefa_editando != num_tarefa:
            # Se há uma tarefa editando diferente da atual, conclua a edição da tarefa anterior
            tarefas[f'-TAREFA-{tarefa_editando}'] = Concluir_edicao(tarefa_editando)
        
        if tarefa_editando == num_tarefa:
            # Se a tarefa em edição é a mesma, conclua a edição
            tarefas[f'-TAREFA-{num_tarefa}'] = Concluir_edicao(num_tarefa)
            tarefa_editando = None
        else:
            # Inicia a edição da nova tarefa
            Habilitar_edicao(num_tarefa)
            tarefa_editando = num_tarefa
    
    elif event.startswith('-EXCLUIR-'):
        num_tarefa = event.split('-')[2]
        if tarefa_editando == num_tarefa:
            tarefa_editando = None  # Reseta a tarefa em edição, se estiver excluindo a que estava sendo editada
        key_check = f'-CHECK-{num_tarefa}'
        key_tarefa = f'-TAREFA-{num_tarefa}'
        key_edit = f'-EDIT-{num_tarefa}'
        key_excluir = f'-EXCLUIR-{num_tarefa}'
        
        # Remove a linha inteira da interface
        janela[key_check].Widget.master.pack_forget()
        janela[key_tarefa].Widget.master.pack_forget()
        janela[key_edit].Widget.master.pack_forget()
        janela[key_excluir].Widget.master.pack_forget()
        
        # Remove a tarefa do dicionário
        if key_tarefa in tarefas:
            del tarefas[key_tarefa]

    # Verifica se o Enter foi pressionado enquanto estava no campo de tarefa
    for key in values:
        if key.startswith('-TAREFA-'):
            num_tarefa = key.split('-')[2]
            if values[key] and tarefa_editando == num_tarefa:  # Se há algo no campo de texto e a tarefa sendo editada é a atual
                tarefas[f'-TAREFA-{num_tarefa}'] = Concluir_edicao(num_tarefa)
                tarefa_editando = None  # Reseta a variável de tarefa em edição

janela.close()