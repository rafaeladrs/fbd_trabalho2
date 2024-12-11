from functools import partial
import tkinter as tk
from tkinter import ttk, messagebox
import mariadb
from datetime import datetime


class Inventario:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventário IF")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)

        self.fonte_texto = ("Arial", 10)
        self.fonte_titulo = ("Arial", 14, "bold")
        self.fonte_subtitulo = ("Arial", 12, "bold")
        self.fonte_pequena = ("Arial", 8)
        
        tk.Label(self.root, text="Inventário do IF", font=self.fonte_titulo).grid(row=0, column=1, columnspan=2, pady=10)
        
        tk.Button(self.root, text="Adicionar Equipamento", command=self.adicionar_equipamento, font=self.fonte_pequena).grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        tk.Button(self.root, text="Visualizar Equipamentos", command=self.visualizar_equipamentos, font=self.fonte_pequena).grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        tk.Button(self.root, text="Adicionar Setor", command=self.adicionar_setor, font=self.fonte_pequena).grid(row=1, column=2, padx=10, pady=10, sticky="ew")
        tk.Button(self.root, text="Visualizar Setores", command=self.visualizar_setores, font=self.fonte_pequena).grid(row=1, column=3, padx=10, pady=10, sticky="ew")
        tk.Button(self.root, text="Visualizar Auditoria", command=self.visualizar_auditoria, font=self.fonte_pequena).grid(row=1, column=4, padx=10, pady=10, sticky="ew")
        tk.Button(self.root, text="Adicionar Campus", command=self.adicionar_campus, font=self.fonte_pequena).grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        tk.Button(self.root, text="Visualizar Campus", command=self.visualizar_campus, font=self.fonte_pequena).grid(row=2, column=1, padx=10, pady=10, sticky="ew")
        tk.Button(self.root, text="Adicionar Fornecedor", command=self.adicionar_fornecedor, font=self.fonte_pequena).grid(row=2, column=2, padx=10, pady=10, sticky="ew")
        tk.Button(self.root, text="Visualizar Fornecedor", command=self.visualizar_fornecedores, font=self.fonte_pequena).grid(row=2, column=3, padx=10, pady=10, sticky="ew")


        self.frame_conteudo = tk.Frame(self.root)
        self.frame_conteudo.grid(row=3, column=0, columnspan=4, pady=20)

        self.treeview = None

    def limpar_conteudo(self):
        for widget in self.frame_conteudo.winfo_children():
            widget.destroy()

    def excluir_em_massa(self, tabela, condicao_sql=None):
        resposta = messagebox.askyesno("Confirmação", "Você realmente deseja excluir TODOS os equipamentos? Esta ação não pode ser desfeita.")

        if resposta:
            conexao = self.conexao_db()
            if conexao:
                cursor = conexao.cursor()
                try:
                    query = f"DELETE FROM {tabela}"
                    if condicao_sql:
                        query += f" {condicao_sql}"
                    cursor.execute(query)
                    conexao.commit()

                    for item in self.treeview.get_children():
                        self.treeview.delete(item)

                    messagebox.showinfo("Sucesso", f"Registros da tabela '{tabela}' excluídos com sucesso.")

                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao excluir registros: {e}")
                finally:
                    conexao.close()
            else:
                messagebox.showerror("Erro", "Erro ao conectar ao banco de dados.")

    def adicionar_equipamento(self):
        self.limpar_conteudo()

        tk.Label(self.frame_conteudo, text="Adicionar Equipamento:", font=self.fonte_subtitulo).grid(row=0, column=1, pady=10)

        tk.Label(self.frame_conteudo, text="Descrição:", font=self.fonte_texto).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.f_descricao = tk.Entry(self.frame_conteudo, width=30)
        self.f_descricao.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.frame_conteudo, text="Status:", font=self.fonte_texto).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        opcoes_status = ["Ativo", "Inativo"]
        self.f_status = ttk.Combobox(self.frame_conteudo, values=opcoes_status, width=27)
        self.f_status.set("Selecione")
        self.f_status.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.frame_conteudo, text="Estado de Conservação:", font=self.fonte_texto).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        opcoes_estado = ["Bom", "Recuperável", "Irrecuperável"]
        self.f_estado_conservacao = ttk.Combobox(self.frame_conteudo, values=opcoes_estado, width=27)
        self.f_estado_conservacao.set("Selecione")
        self.f_estado_conservacao.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(self.frame_conteudo, text="Setores:", font=self.fonte_texto).grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.f_setor = tk.Listbox(self.frame_conteudo, selectmode="multiple", width=27)
        self.carregar_setores(self.f_setor)
        self.f_setor.grid(row=4, column=1, padx=10, pady=10)

        tk.Label(self.frame_conteudo, text="Valor de Aquisição (R$):", font=self.fonte_texto).grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.f_valor_aquisicao = tk.Entry(self.frame_conteudo, width=30)
        self.f_valor_aquisicao.grid(row=5, column=1, padx=10, pady=10)

        tk.Label(self.frame_conteudo, text="Valor Depreciado (R$):", font=self.fonte_texto).grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.f_valor_depreciado = tk.Entry(self.frame_conteudo, width=30)
        self.f_valor_depreciado.grid(row=6, column=1, padx=10, pady=10)

        tk.Label(self.frame_conteudo, text="Número da Nota Fiscal:", font=self.fonte_texto).grid(row=7, column=0, padx=10, pady=10, sticky="w")
        self.f_numero_nota_fiscal = tk.Entry(self.frame_conteudo, width=30)
        self.f_numero_nota_fiscal.grid(row=7, column=1, padx=10, pady=10)

        tk.Label(self.frame_conteudo, text="Número de Série:", font=self.fonte_texto).grid(row=8, column=0, padx=10, pady=10, sticky="w")
        self.f_numero_serie = tk.Entry(self.frame_conteudo, width=30)
        self.f_numero_serie.grid(row=8, column=1, padx=10, pady=10)

        tk.Button(self.frame_conteudo, text="Registrar", command=self.registrar_equipamento, font=self.fonte_subtitulo).grid(row=9, column=1, pady=20)

    def registrar_equipamento(self):
        descricao = self.f_descricao.get()
        status = self.f_status.get()
        setores_selecionados = self.f_setor.curselection()
        estado_conservacao = self.f_estado_conservacao.get()
        valor_aquisicao = self.f_valor_aquisicao.get()
        valor_depreciado = self.f_valor_depreciado.get()
        numero_nota_fiscal = self.f_numero_nota_fiscal.get()
        numero_serie = self.f_numero_serie.get()

        if not descricao or status == "Selecione" or estado_conservacao == "Selecione":
            tk.messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
            return

        try:
            conexao = self.conexao_db()
            if conexao:
                cursor = conexao.cursor()
                query = """
                        INSERT INTO equipamento 
                        (Descricao, Status, Estado_Conservacao, Valor_Aquisicao, Valor_Depreciado, Numero_Nota_Fiscal, Numero_de_serie)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """
                valores = (
                    descricao,
                    status,
                    estado_conservacao,
                    float(valor_aquisicao),
                    float(valor_depreciado),
                    int(numero_nota_fiscal),
                    int(numero_serie)
                )
                cursor.execute(query, valores)
                conexao.commit()

                id_equipamento = cursor.lastrowid
                for setor_index in setores_selecionados:
                    setor_nome = self.f_setor.get(setor_index)
                    
                    cursor.execute("SELECT ID_Setor FROM setor WHERE Nome_Setor = ?", (setor_nome,))
                    id_setor = cursor.fetchone()

                    if id_setor:  
                        id_setor = id_setor[0]
                        
                        query_relacionamento = """
                            INSERT INTO equipamento_setor (ID_Equipamento, ID_Setor)
                            VALUES (?, ?)
                        """
                        cursor.execute(query_relacionamento, (id_equipamento, id_setor))
                        conexao.commit()
                    else:
                        print(f"Setor {setor_nome} não encontrado.")
            tk.messagebox.showinfo("Sucesso", "Equipamento registrado com sucesso!")
            conexao.close()
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao inserir no banco: {e}")

    def visualizar_por_estado(self):
        conexao = self.conexao_db()
        if conexao:
            cursor = conexao.cursor()
            query_estado_conservacao = """
                SELECT e.Estado_Conservacao, COUNT(*) AS Total_Equipamentos
                FROM equipamento e
                GROUP BY e.Estado_Conservacao
            """
            cursor.execute(query_estado_conservacao)
            equipamentos_por_estado = cursor.fetchall()

            janela_estado = tk.Toplevel(self.root)
            janela_estado.title("Equipamentos por Estado de Conservação")

            treeview_estado = ttk.Treeview(janela_estado, columns=("Estado de Conservação", "Total Equipamentos"), show="headings")
            treeview_estado.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            treeview_estado.heading("Estado de Conservação", text="Estado de Conservação")
            treeview_estado.heading("Total Equipamentos", text="Total Equipamentos")

            for estado, total in equipamentos_por_estado:
                treeview_estado.insert("", "end", values=(estado, total))
            
            treeview_estado.column("Estado de Conservação", width=200)
            treeview_estado.column("Total Equipamentos", width=150)

            tk.Button(janela_estado, text="Fechar", command=janela_estado.destroy).grid(row=1, column=0, padx=10, pady=10)

            conexao.close()
        else:
            messagebox.showerror("Erro", "Erro ao conectar ao banco de dados.")

    def visualizar_equipamentos(self):
        self.limpar_conteudo()

        conexao = self.conexao_db()
        if conexao:
            cursor = conexao.cursor()
            query = """
                    SELECT e.ID_Equipamento, e.Descricao, e.Status, e.Estado_Conservacao, e.Valor_Aquisicao, 
                        e.Valor_Depreciado, e.Numero_Nota_Fiscal, e.Numero_de_serie, GROUP_CONCAT(s.Nome_Setor) AS Setores
                    FROM equipamento e
                    JOIN equipamento_setor es ON e.ID_Equipamento = es.ID_Equipamento
                    JOIN setor s ON es.ID_Setor = s.ID_Setor
                    GROUP BY e.ID_Equipamento
                    """
            cursor.execute(query)
            equipamentos = cursor.fetchall()
            for widget in self.frame_conteudo.winfo_children():
                widget.destroy()

            self.treeview = ttk.Treeview(self.frame_conteudo, columns=("ID", "Descrição", "Status", "Estado", "Valor Aquisição", 
                                                                "Valor Depreciado", "Número Nota Fiscal", "Número Série", "Setores"), 
                                                                show="headings")
            self.treeview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            self.treeview.heading("ID", text="ID")
            self.treeview.heading("Descrição", text="Descrição")
            self.treeview.heading("Status", text="Status")
            self.treeview.heading("Estado", text="Estado de Conservação")
            self.treeview.heading("Valor Aquisição", text="Valor Aquisição")
            self.treeview.heading("Valor Depreciado", text="Valor Depreciado")
            self.treeview.heading("Número Nota Fiscal", text="Número Nota Fiscal")
            self.treeview.heading("Número Série", text="Número Série")
            self.treeview.heading("Setores", text="Setores") 

            for equipamento in equipamentos:
                self.treeview.insert("", "end", values=equipamento)

            for col in self.treeview["columns"]:
                self.treeview.column(col, width=100)

            self.frame_conteudo.grid_rowconfigure(0, weight=1)
            self.frame_conteudo.grid_columnconfigure(0, weight=1)

            tk.Button(self.frame_conteudo, text="Excluir Equipamento", command=self.excluir_equipamento, font=self.fonte_pequena).grid(row=1, column=0, padx=10, pady=10)
            tk.Button(self.frame_conteudo, text="Excluir em massa", command=partial(self.excluir_em_massa, "equipamento"), font=self.fonte_pequena).grid(row=2, column=0, padx=10, pady=10)
            tk.Button(self.frame_conteudo, text="Adicionar Equipamento", command=self.adicionar_equipamento, font=self.fonte_pequena).grid(row=3, column=0, padx=10, pady=10)
            tk.Button(self.frame_conteudo, text="Editar Equipamento", command=self.editar_equipamento, font=self.fonte_pequena).grid(row=4, column=0, padx=10, pady=10)
            tk.Button(self.frame_conteudo, text="Visualizar Equipamentos por Estado", command=self.visualizar_por_estado, font=self.fonte_pequena).grid(row=5, column=0, padx=10, pady=10)

            self.frame_conteudo.update_idletasks()
            conexao.close()
        else:
            messagebox.showerror("Erro", "Erro ao conectar ao banco de dados.")
      
    def excluir_equipamento(self):
        selecionado = self.treeview.selection()
        if not selecionado:
            messagebox.showwarning("Seleção", "Selecione um equipamento para excluir.")
            return

        item = selecionado[0]
        id_equipamento = self.treeview.item(item, "values")[0]

        conexao = self.conexao_db()
        if conexao:
            cursor = conexao.cursor()
            try:
                query = "DELETE FROM equipamento WHERE id = ?"
                cursor.execute(query, (id_equipamento,))
                conexao.commit()

                self.treeview.delete(item)
                
                messagebox.showinfo("Sucesso", "Equipamento excluído com sucesso.")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir equipamento: {e}")
            finally:
                conexao.close()
        else:
            messagebox.showerror("Erro", "Erro ao conectar ao banco de dados.")

        descricao = self.f_descricao.get()
        status = self.f_status.get()
        estado_conservacao = self.f_estado_conservacao.get()
        valor_aquisicao = self.f_valor_aquisicao.get()
        valor_depreciado = self.f_valor_depreciado.get()
        numero_nota_fiscal = self.f_numero_nota_fiscal.get()
        numero_serie = self.f_numero_serie.get()

        if not descricao or status == "Selecione" or estado_conservacao == "Selecione":
            tk.messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
            return
        
        try:
            conexao = self.conexao_db()
            if conexao:
                cursor = conexao.cursor()

                if id_equipamento:
                    query = """
                            UPDATE equipamento 
                            SET Descricao = ?, Status = ?, Estado_Conservacao = ?, 
                                Valor_Aquisicao = ?, Valor_Depreciado = ?, 
                                Numero_Nota_Fiscal = ?, Numero_de_serie = ?
                            WHERE ID_Equipamento = ?
                        """
                    valores = (
                        descricao,
                        status,
                        estado_conservacao,
                        float(valor_aquisicao),
                        float(valor_depreciado),
                        int(numero_nota_fiscal),
                        int(numero_serie),
                        id_equipamento  
                    )
                    cursor.execute(query, valores)
                    conexao.commit()
                    tk.messagebox.showinfo("Sucesso", "Equipamento atualizado com sucesso!")
                else:  
                    query = """
                            INSERT INTO equipamento 
                            (Descricao, Status, Estado_Conservacao, Valor_Aquisicao, Valor_Depreciado, Numero_Nota_Fiscal, Numero_de_serie)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        """
                    valores = (
                        descricao,
                        status,
                        estado_conservacao,
                        float(valor_aquisicao),
                        float(valor_depreciado),
                        int(numero_nota_fiscal),
                        int(numero_serie)
                    )
                    cursor.execute(query, valores)
                    conexao.commit()
                    tk.messagebox.showinfo("Sucesso", "Equipamento registrado com sucesso!")
                conexao.close()
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao salvar no banco: {e}")

    def editar_equipamento(self):
        item_selecionado = self.treeview.selection()

        if not item_selecionado:
            messagebox.showwarning("Atenção", "Nenhum equipamento selecionado para edição.")
            return

        valores = self.treeview.item(item_selecionado[0], "values")
        id_equipamento = valores[0]
        descricao = valores[1]
        status = valores[2]
        estado_conservacao = valores[3]
        valor_aquisicao = valores[4]
        valor_depreciado = valores[5]
        numero_nota_fiscal = valores[6]
        numero_serie = valores[7]

        editar_window = tk.Toplevel(self.root)
        editar_window.title("Editar Equipamento")

        tk.Label(editar_window, text="Descrição:").grid(row=0, column=0, padx=10, pady=5)
        descricao_entry = tk.Entry(editar_window)
        descricao_entry.insert(0, descricao)
        descricao_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(editar_window, text="Status:").grid(row=1, column=0, padx=10, pady=5)
        opcoes_status = ["Ativo", "Inativo"]
        status_combobox = ttk.Combobox(editar_window, values=opcoes_status, width=27)
        status_combobox.set(status)
        status_combobox.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(editar_window, text="Estado de Conservação:").grid(row=2, column=0, padx=10, pady=5)
        opcoes_estado = ["Bom", "Recuperável", "Irrecuperável"]
        estado_combobox = ttk.Combobox(editar_window, values=opcoes_estado, width=27)
        estado_combobox.set(estado_conservacao)
        estado_combobox.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(editar_window, text="Valor de Aquisição (R$):").grid(row=3, column=0, padx=10, pady=5)
        valor_aquisicao_entry = tk.Entry(editar_window)
        valor_aquisicao_entry.insert(0, valor_aquisicao)
        valor_aquisicao_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(editar_window, text="Valor Depreciado (R$):").grid(row=4, column=0, padx=10, pady=5)
        valor_depreciado_entry = tk.Entry(editar_window)
        valor_depreciado_entry.insert(0, valor_depreciado)
        valor_depreciado_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(editar_window, text="Número da Nota Fiscal:").grid(row=5, column=0, padx=10, pady=5)
        numero_nota_fiscal_entry = tk.Entry(editar_window)
        numero_nota_fiscal_entry.insert(0, numero_nota_fiscal)
        numero_nota_fiscal_entry.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(editar_window, text="Número de Série:").grid(row=6, column=0, padx=10, pady=5)
        numero_serie_entry = tk.Entry(editar_window)
        numero_serie_entry.insert(0, numero_serie)
        numero_serie_entry.grid(row=6, column=1, padx=10, pady=5)

        def salvar_edicao():
            novo_descricao = descricao_entry.get()
            novo_status = status_combobox.get()
            novo_estado = estado_combobox.get()
            novo_valor_aquisicao = valor_aquisicao_entry.get()
            novo_valor_depreciado = valor_depreciado_entry.get()
            novo_numero_nota_fiscal = numero_nota_fiscal_entry.get()
            novo_numero_serie = numero_serie_entry.get()

            if not novo_descricao or novo_status == "Selecione" or novo_estado == "Selecione":
                messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")
                return

            try:
                conexao = self.conexao_db()
                if conexao:
                    cursor = conexao.cursor()
                    query = """
                            UPDATE equipamento 
                            SET Descricao = ?, Status = ?, Estado_Conservacao = ?, 
                                Valor_Aquisicao = ?, Valor_Depreciado = ?, 
                                Numero_Nota_Fiscal = ?, Numero_de_serie = ?
                            WHERE ID_Equipamento = ?
                        """
                    valores = (
                        novo_descricao,
                        novo_status,
                        novo_estado,
                        float(novo_valor_aquisicao),
                        float(novo_valor_depreciado),
                        int(novo_numero_nota_fiscal),
                        int(novo_numero_serie),
                        id_equipamento
                    )
                    cursor.execute(query, valores)
                    conexao.commit()

                    self.treeview.item(item_selecionado[0], values=(id_equipamento, novo_descricao, novo_status, novo_estado, novo_valor_aquisicao, novo_valor_depreciado, novo_numero_nota_fiscal, novo_numero_serie))

                    messagebox.showinfo("Sucesso", "Equipamento atualizado com sucesso.")
                    editar_window.destroy()

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao atualizar equipamento: {e}")
            finally:
                conexao.close()

        tk.Button(editar_window, text="Salvar", command=salvar_edicao).grid(row=7, column=0, columnspan=2, pady=10)

    def adicionar_setor(self):
        self.limpar_conteudo()

        tk.Label(self.frame_conteudo, text="Adicionar Setor:", font=self.fonte_subtitulo).grid(row=0, column=1, pady=10)

        tk.Label(self.frame_conteudo, text="Nome do Setor:", font=self.fonte_texto).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.f_nome_setor = tk.Entry(self.frame_conteudo, width=30)
        self.f_nome_setor.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.frame_conteudo, text="Responsável:", font=self.fonte_texto).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.f_responsavel = tk.Entry(self.frame_conteudo, width=30)
        self.f_responsavel.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.frame_conteudo, text="Selecione Salas:", font=self.fonte_texto).grid(row=3, column=0, padx=10, pady=10)
        self.f_salas_listbox = tk.Listbox(self.frame_conteudo, selectmode=tk.MULTIPLE, height=5)
        self.f_salas_listbox.grid(row=3, column=1, padx=10, pady=10)
        self.carregar_salas(self.f_salas_listbox)

        tk.Button(self.frame_conteudo, text="Adicionar Sala", command=self.abrir_janela_adicionar_sala, font=self.fonte_subtitulo).grid(row=4, column=1, padx=10, pady=10)
        tk.Button(self.frame_conteudo, text="Registrar", command=self.registrar_setor, font=self.fonte_subtitulo).grid(row=5, column=1, padx=10, pady=10)

    def registrar_setor(self):
        nome_setor = self.f_nome_setor.get()
        responsavel = self.f_responsavel.get()

        if not nome_setor or not responsavel:
            tk.messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
            return

        salas_selecionadas = [self.f_salas_listbox.get(i) for i in self.f_salas_listbox.curselection()]

        try:
            conexao = self.conexao_db()
            if conexao:
                cursor = conexao.cursor()
                query = """
                        INSERT INTO setor 
                        (Nome_Setor, Responsavel)
                        VALUES (?, ?)
                    """
                valores = (nome_setor, responsavel)
                cursor.execute(query, valores)
                conexao.commit()

                id_setor = cursor.lastrowid
                for sala_nome in salas_selecionadas:
                    cursor.execute("SELECT ID_Sala FROM sala WHERE Nome = ?", (sala_nome,))
                    sala_id = cursor.fetchone()[0]
                    cursor.execute("""
                            INSERT INTO setor_sala (ID_Setor, ID_Sala)
                            VALUES (?, ?)
                        """, (id_setor, sala_id))
                conexao.commit()

                tk.messagebox.showinfo("Sucesso", "Setor registrado com sucesso!")
                conexao.close()
                self.carregar_salas(self.f_salas_listbox)
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao inserir no banco: {e}")

    def visualizar_setores(self):
        self.limpar_conteudo()

        conexao = self.conexao_db()
        if conexao:
            cursor = conexao.cursor()
            query = "SELECT * FROM setor"
            cursor.execute(query)
            setores = cursor.fetchall()

            self.treeview = ttk.Treeview(self.frame_conteudo, columns=("ID", "Nome", "Responsável", "Total Equipamentos"), show="headings")
            self.treeview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            self.treeview.heading("ID", text="ID")
            self.treeview.heading("Nome", text="Nome do Setor")
            self.treeview.heading("Responsável", text="Responsável")
            self.treeview.heading("Total Equipamentos", text="Total de Equipamentos")

            for setor in setores:
                self.treeview.insert("", "end", values=setor)

            for col in self.treeview["columns"]:
                self.treeview.column(col, width=150)

            self.frame_conteudo.grid_rowconfigure(0, weight=1)
            self.frame_conteudo.grid_columnconfigure(0, weight=1)

            tk.Button(self.frame_conteudo, text="Excluir Setor", command=self.excluir_setor, font=self.fonte_pequena).grid(row=1, column=0, padx=10, pady=10)
            tk.Button(self.frame_conteudo, text="Excluir em massa", command=partial(self.excluir_em_massa, "setor"), font=self.fonte_pequena).grid(row=2, column=0, padx=10, pady=10)
            tk.Button(self.frame_conteudo, text="Editar Setor", command=self.editar_setor, font=self.fonte_pequena).grid(row=3, column=0, padx=10, pady=10)

            conexao.close()
        else:
            messagebox.showerror("Erro", "Erro ao conectar ao banco de dados.")

    def excluir_setor(self):
        selecionado = self.treeview.selection()
        if not selecionado:
            messagebox.showwarning("Seleção", "Selecione um setor para excluir.")
            return

        item = selecionado[0]
        id_setor = self.treeview.item(item, "values")[0]

        conexao = self.conexao_db()
        if conexao:
            cursor = conexao.cursor()
            try:
                query = "DELETE FROM setor WHERE ID_Setor = ?"
                cursor.execute(query, (id_setor,))
                conexao.commit()

                self.treeview.delete(item)
                messagebox.showinfo("Sucesso", "Setor excluído com sucesso.")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir setor: {e}")
            finally:
                conexao.close()
        else:
            messagebox.showerror("Erro", "Erro ao conectar ao banco de dados.")

    def editar_setor(self):
        item_selecionado = self.treeview.selection()

        if not item_selecionado:
            messagebox.showwarning("Atenção", "Nenhum setor selecionado para edição.")
            return

        valores = self.treeview.item(item_selecionado[0], "values")
        id_setor = valores[0]
        nome_setor = valores[1]
        responsavel = valores[2]

        editar_window = tk.Toplevel(self.root)
        editar_window.title("Editar Setor")

        tk.Label(editar_window, text="Nome do Setor:").grid(row=0, column=0, padx=10, pady=5)
        nome_entry = tk.Entry(editar_window)
        nome_entry.insert(0, nome_setor)
        nome_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(editar_window, text="Responsável:").grid(row=1, column=0, padx=10, pady=5)
        responsavel_entry = tk.Entry(editar_window)
        responsavel_entry.insert(0, responsavel)
        responsavel_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(editar_window, text="Salas Associadas:").grid(row=2, column=0, padx=10, pady=5)
        salas_listbox = tk.Listbox(editar_window, selectmode=tk.MULTIPLE, height=5)
        salas_listbox.grid(row=2, column=1, padx=10, pady=5)

        self.carregar_salas_associadas(id_setor, salas_listbox)

        def carregar_salas_associadas(id_setor, listbox):
            listbox.delete(0, tk.END)
            try:
                conexao = self.conexao_db()
                if conexao:
                    cursor = conexao.cursor()
                    query = """
                        SELECT sala.Nome 
                        FROM sala 
                        JOIN setor_sala ON sala.ID_Sala = setor_sala.ID_Sala
                        WHERE setor_sala.ID_Setor = ?
                    """
                    cursor.execute(query, (id_setor,))
                    salas = cursor.fetchall()

                    for sala in salas:
                        listbox.insert(tk.END, sala[0])

                    conexao.close()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar salas associadas: {e}")

        def salvar_edicao():
            novo_nome = nome_entry.get() 
            novo_responsavel = responsavel_entry.get()  

            if not novo_nome or not novo_responsavel:
                messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")
                return
            
            salas_selecionadas = [salas_listbox.get(i) for i in salas_listbox.curselection()]

            conexao = self.conexao_db()
            if conexao:
                cursor = conexao.cursor()
                try:
                    query = "UPDATE setor SET Nome_Setor = ?, Responsavel = ? WHERE ID_Setor = ?"
                    cursor.execute(query, (novo_nome, novo_responsavel, id_setor))

                    cursor.execute("DELETE FROM setor_sala WHERE ID_Setor = ?", (id_setor,))

                    for sala_nome in salas_selecionadas:
                        cursor.execute("""
                            SELECT ID_Sala FROM sala WHERE Nome = ?
                        """, (sala_nome,))
                        sala_id = cursor.fetchone()[0]
                        cursor.execute("""
                            INSERT INTO setor_sala (ID_Setor, ID_Sala)
                            VALUES (?, ?)
                        """, (id_setor, sala_id))

                    conexao.commit()

                    self.treeview.item(item_selecionado[0], values=(id_setor, novo_nome, novo_responsavel))

                    messagebox.showinfo("Sucesso", "Setor atualizado com sucesso.")
                    editar_window.destroy()

                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao atualizar setor: {e}")
                finally:
                    conexao.close()

        tk.Button(editar_window, text="Salvar", command=salvar_edicao).grid(row=3, column=0, columnspan=2, pady=10)

    def abrir_janela_adicionar_sala(self):
        janela_sala = tk.Toplevel(self.root)
        janela_sala.title("Adicionar Nova Sala")

        tk.Label(janela_sala, text="Nome da Sala:", font=self.fonte_texto).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        nome_sala_entry = tk.Entry(janela_sala, width=30)
        nome_sala_entry.grid(row=0, column=1, padx=10, pady=10)
        def salvar_sala():
            nome_sala = nome_sala_entry.get()

            if not nome_sala:
                messagebox.showwarning("Atenção", "Por favor, preencha o nome da sala.")
                return
            
            try:
                conexao = self.conexao_db()
                if conexao:
                    cursor = conexao.cursor()
                    query = """
                            INSERT INTO sala (Nome) 
                            VALUES (?);
                        """
                    cursor.execute(query, (nome_sala,))
                    conexao.commit()
                    messagebox.showinfo("Sucesso", "Sala registrada com sucesso!")
                    janela_sala.destroy()
                    self.carregar_salas(self.f_salas_listbox)
                    conexao.close()

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao inserir no banco: {e}")

        tk.Button(janela_sala, text="Salvar", command=salvar_sala, font=self.fonte_subtitulo).grid(row=1, column=1, padx=10, pady=10)
    
    def salvar_sala(self):
        nome_sala = tk.nome_sala_entry.get()

        if not nome_sala:
            messagebox.showwarning("Atenção", "Por favor, preencha o nome da sala.")
            return
        
        try:
            conexao = self.conexao_db()
            if conexao:
                cursor = conexao.cursor()
                query = """
                        INSERT INTO sala (Nome) 
                        VALUES (?);
                    """
                cursor.execute(query, (nome_sala,))
                conexao.commit()

                self.carregar_salas(self.f_salas_listbox)
                
                messagebox.showinfo("Sucesso", "Sala registrada com sucesso!")
                tk.janela_sala.destroy()
                conexao.close()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir no banco: {e}")

    def carregar_salas(self, listbox):
        listbox.delete(0, tk.END)  

        try:
            conexao = self.conexao_db()
            if conexao:
                cursor = conexao.cursor()
                query = """
                        SELECT Nome 
                        FROM sala 
                        WHERE ID_Sala NOT IN (SELECT ID_Sala FROM setor_sala)
                        """
                cursor.execute(query)
                salas = cursor.fetchall()

                for sala in salas:
                    listbox.insert(tk.END, sala[0])

                conexao.close()
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Erro ao carregar salas: {e}")

    def carregar_setores(self, destino):
        conexao = self.conexao_db()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT Nome_Setor FROM setor")
            setores = cursor.fetchall()
            
            setores_lista = [setor[0] for setor in setores]
        
        if isinstance(destino, tk.Listbox): 
            destino.delete(0, tk.END) 
            for setor in setores_lista:
                destino.insert(tk.END, setor) 
        
        elif isinstance(destino, tk.ttk.Combobox):  
            destino['values'] = setores_lista

        conexao.close()

    def carregar_setores_campus(self, destino):
        conexao = self.conexao_db()
        if conexao:
            cursor = conexao.cursor()
            cursor.execute("""
                        SELECT s.Nome_Setor 
                        FROM setor s
                        LEFT JOIN edificio_setor_campus esc ON s.ID_Setor = esc.ID_Setor
                        WHERE esc.ID_Campus IS NULL OR esc.ID_Campus = 0
                        """)
            setores = cursor.fetchall()
            
            setores_lista = [setor[0] for setor in setores]

            if isinstance(destino, tk.Listbox): 
                destino.delete(0, tk.END)
                for setor in setores_lista:
                    destino.insert(tk.END, setor) 
            
            elif isinstance(destino, tk.ttk.Combobox):  
                destino['values'] = setores_lista

            conexao.close()

    def adicionar_campus(self):
        self.limpar_conteudo()

        tk.Label(self.frame_conteudo, text="Adicionar Campus:", font=self.fonte_subtitulo).grid(row=0, column=1, pady=10)
        tk.Label(self.frame_conteudo, text="Nome do Campus", font=self.fonte_texto).grid(row=1, column=0, padx=10, pady=10)
        nome_entry = tk.Entry(self.frame_conteudo, font=self.fonte_texto)
        nome_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.frame_conteudo, text="Endereço", font=self.fonte_texto).grid(row=2, column=0, padx=10, pady=10)
        endereco_entry = tk.Entry(self.frame_conteudo, font=self.fonte_texto)
        endereco_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.frame_conteudo, text="Selecione Setores:", font=self.fonte_texto).grid(row=3, column=0, padx=10, pady=10)
        self.setores_listbox = tk.Listbox(self.frame_conteudo, selectmode=tk.MULTIPLE, height=15)
        self.setores_listbox.grid(row=3, column=1, padx=10, pady=10, rowspan=2)

        self.carregar_setores_campus(self.setores_listbox)

        def salvar_campus():
            nome = nome_entry.get()
            endereco = endereco_entry.get()

            if not nome or not endereco:
                messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")
                return
            
            setores_selecionados = [self.setores_listbox.get(i) for i in self.setores_listbox.curselection()]
            conexao = self.conexao_db()
            if conexao:
                cursor = conexao.cursor()
                try:
                    query = "INSERT INTO campus (Nome_Campus, Endereco) VALUES (%s, %s)"
                    cursor.execute(query, (nome, endereco))
                    campus_id = cursor.lastrowid
                    conexao.commit()

                    for setor in setores_selecionados:
                        query_setor = """
                            INSERT INTO edificio_setor_campus (ID_Campus, ID_Setor)
                            SELECT %s, ID_Setor 
                            FROM setor 
                            WHERE Nome_Setor = %s
                            """
                        cursor.execute(query_setor, (campus_id, setor))
                    conexao.commit()
                    
                    messagebox.showinfo("Sucesso", "Campus adicionado com sucesso.")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao adicionar campus: {e}")
                finally:
                    conexao.close()
            else:
                messagebox.showerror("Erro", "Erro ao conectar ao banco de dados.")
        tk.Button(self.frame_conteudo, text="Salvar", command=salvar_campus, font=self.fonte_pequena).grid(row=5, column=0, columnspan=2, pady=10)

    def visualizar_equipamentos_campus(self):
        conexao = self.conexao_db()
        if conexao:
            cursor = conexao.cursor()
            query = """
                SELECT 
                    c.Nome_Campus,
                    s.Nome_Setor,
                    e.Descricao AS Equipamento,
                    e.Status,
                    e.Estado_Conservacao
                FROM edificio_setor_campus esc
                JOIN campus c ON esc.ID_Campus = c.ID_Campus
                JOIN setor s ON esc.ID_Setor = s.ID_Setor
                JOIN equipamento_setor es ON s.ID_Setor = es.ID_Setor
                JOIN equipamento e ON es.ID_Equipamento = e.ID_Equipamento
            """
            cursor.execute(query)
            equipamentos = cursor.fetchall()
            equipamentos_window = tk.Toplevel(self.root)
            equipamentos_window.title("Equipamentos por Campus")

            treeview = ttk.Treeview(equipamentos_window, columns=("Campus", "Setor", "Equipamento", "Status", "Conservação"), show="headings")
            treeview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            treeview.heading("Campus", text="Nome do Campus")
            treeview.heading("Setor", text="Nome do Setor")
            treeview.heading("Equipamento", text="Equipamento")
            treeview.heading("Status", text="Status")
            treeview.heading("Conservação", text="Estado de Conservação")

            for col in treeview["columns"]:
                treeview.column(col, width=150)

            for item in equipamentos:
                treeview.insert("", "end", values=item)

            conexao.close()
        else:
            messagebox.showerror("Erro", "Erro ao conectar ao banco de dados.")

    def visualizar_campus(self):
        self.limpar_conteudo()

        conexao = self.conexao_db()
        if conexao:
            cursor = conexao.cursor()
            query = """
                SELECT c.ID_Campus, c.Nome_Campus, c.Endereco, 
                GROUP_CONCAT(s.Nome_Setor SEPARATOR ', ') AS Setores
                FROM campus c
                LEFT JOIN edificio_setor_campus esc ON c.ID_Campus = esc.ID_Campus
                LEFT JOIN setor s ON esc.ID_Setor = s.ID_Setor
                GROUP BY c.ID_Campus
            """
            cursor.execute(query)
            campus = cursor.fetchall()

            for widget in self.frame_conteudo.winfo_children():
                widget.destroy()

            self.treeview = ttk.Treeview(self.frame_conteudo, columns=("ID", "Setores", "Nome", "Endereço"), show="headings")
            self.treeview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            self.treeview.heading("ID", text="ID")
            self.treeview.heading("Setores", text="Setores")
            self.treeview.heading("Nome", text="Nome do Campus")
            self.treeview.heading("Endereço", text="Endereço")

            for col in self.treeview["columns"]:
                self.treeview.column(col, width=150)

            for item in campus:
                endereco = item[2] if item[2] is not None else "Endereço não informado"
                setores = item[3] if item[3] is not None else "Sem setores"
                
                self.treeview.insert("", "end", values=(item[0], setores, item[1], endereco))

            tk.Button(self.frame_conteudo, text="Excluir Campus", command=self.excluir_campus, font=self.fonte_pequena).grid(row=1, column=0, padx=10, pady=10)
            tk.Button(self.frame_conteudo, text="Excluir em Massa", command=lambda: self.excluir_em_massa("campus"), font=self.fonte_pequena).grid(row=2, column=0, padx=10, pady=10)
            tk.Button(self.frame_conteudo, text="Adicionar Campus", command=self.adicionar_campus, font=self.fonte_pequena).grid(row=3, column=0, padx=10, pady=10)
            tk.Button(self.frame_conteudo, text="Editar Campus", command=self.editar_campus, font=self.fonte_pequena).grid(row=4, column=0, padx=10, pady=10)
            tk.Button(self.frame_conteudo, text="Visualizar Equipamentos Por Campus", command=self.visualizar_equipamentos_campus, font=self.fonte_pequena).grid(row=5, column=0, padx=10, pady=10)

            conexao.close()
        else:
            messagebox.showerror("Erro", "Erro ao conectar ao banco de dados.")
   
    def excluir_campus(self):
        item_selecionado = self.treeview.selection()

        if not item_selecionado:
            messagebox.showwarning("Atenção", "Nenhum campus selecionado para exclusão.")
            return

        resposta = messagebox.askyesno("Confirmação", "Deseja realmente excluir o campus selecionado?")

        if resposta:
            conexao = self.conexao_db()
            if conexao:
                cursor = conexao.cursor()
                try:
                    for item in item_selecionado:
                        valores = self.treeview.item(item, "values")
                        id_campus = valores[0]

                        query = "DELETE FROM campus WHERE ID_Campus = %s"
                        cursor.execute(query, (id_campus,))

                        self.treeview.delete(item)

                    conexao.commit()
                    messagebox.showinfo("Sucesso", "Campus excluído com sucesso.")

                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao excluir campus: {e}")
                finally:
                    conexao.close()
            else:
                messagebox.showerror("Erro", "Erro ao conectar ao banco de dados.")

    def editar_campus(self):
        item_selecionado = self.treeview.selection()

        if not item_selecionado:
            messagebox.showwarning("Atenção", "Nenhum campus selecionado para edição.")
            return

        valores = self.treeview.item(item_selecionado[0], "values")
        id_campus = valores[0]
        nome_campus = valores[1]
        endereco_campus = valores[2]

        editar_window = tk.Toplevel(self.root)
        editar_window.title("Editar Campus")

        tk.Label(editar_window, text="Nome do Campus:").grid(row=0, column=0, padx=10, pady=5)
        nome_entry = tk.Entry(editar_window)
        nome_entry.insert(0, nome_campus)
        nome_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(editar_window, text="Endereço:").grid(row=1, column=0, padx=10, pady=5)
        endereco_entry = tk.Entry(editar_window)
        endereco_entry.insert(0, endereco_campus)
        endereco_entry.grid(row=1, column=1, padx=10, pady=5)

        def salvar_edicao():
            novo_nome = nome_entry.get()
            novo_endereco = endereco_entry.get()

            if not novo_nome or not novo_endereco:
                messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")
                return

            conexao = self.conexao_db()
            if conexao:
                cursor = conexao.cursor()
                try:
                    query = "UPDATE campus SET Nome_Campus = %s, Endereco = %s WHERE ID_Campus = %s"
                    cursor.execute(query, (novo_nome, novo_endereco, id_campus))
                    conexao.commit()
                    messagebox.showinfo("Sucesso", "Campus atualizado com sucesso.")

                    self.treeview.item(item_selecionado[0], values=(id_campus, novo_nome, novo_endereco))

                    editar_window.destroy()

                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao atualizar campus: {e}")
                finally:
                    conexao.close()
            else:
                messagebox.showerror("Erro", "Erro ao conectar ao banco de dados.")

        tk.Button(editar_window, text="Salvar", command=salvar_edicao).grid(row=2, column=0, columnspan=2, pady=10)

    def visualizar_fornecedores(self):
        self.limpar_conteudo()

        conexao = self.conexao_db()
        if conexao:
            cursor = conexao.cursor()
            query = """
                    SELECT f.ID_Fornecedor, f.Nome_Fornecedor, f.Contato, c.Nome_Campus
                    FROM fornecedor f
                    LEFT JOIN fornecedor_campus fc ON f.ID_Fornecedor = fc.ID_Fornecedor
                    LEFT JOIN campus c ON fc.ID_Campus = c.ID_Campus
                    """
            cursor.execute(query)
            fornecedores = cursor.fetchall()

            for widget in self.frame_conteudo.winfo_children():
                widget.destroy()

            self.treeview = ttk.Treeview(self.frame_conteudo, columns=("ID", "Nome", "Contato", "Campus"), show="headings")
            self.treeview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            self.treeview.heading("ID", text="ID")
            self.treeview.heading("Nome", text="Nome do Fornecedor")
            self.treeview.heading("Contato", text="Contato")
            self.treeview.heading("Campus", text="Campus Relacionados")

            for fornecedor in fornecedores:
                self.treeview.insert("", "end", values=fornecedor)

            for col in self.treeview["columns"]:
                self.treeview.column(col, width=150)

            self.frame_conteudo.grid_rowconfigure(0, weight=1)
            self.frame_conteudo.grid_columnconfigure(0, weight=1)

            tk.Button(self.frame_conteudo, text="Excluir Fornecedor", command=self.excluir_fornecedor, font=self.fonte_pequena).grid(row=1, column=0, padx=10, pady=10)
            tk.Button(self.frame_conteudo, text="Excluir em Massa", command=lambda: self.excluir_em_massa("fornecedor"), font=self.fonte_pequena).grid(row=2, column=0, padx=10, pady=10)
            tk.Button(self.frame_conteudo, text="Adicionar Fornecedor", command=self.adicionar_fornecedor, font=self.fonte_pequena).grid(row=3, column=0, padx=10, pady=10)
            tk.Button(self.frame_conteudo, text="Editar Fornecedor", command=self.editar_fornecedor, font=self.fonte_pequena).grid(row=4, column=0, padx=10, pady=10)

            conexao.close()

    def excluir_fornecedor(self):
        item_selecionado = self.treeview.selection()

        if not item_selecionado:
            messagebox.showwarning("Atenção", "Nenhum fornecedor selecionado para exclusão.")
            return

        resposta = messagebox.askyesno("Confirmação", "Deseja realmente excluir o fornecedor selecionado?")

        if resposta:
            conexao = self.conexao_db()
            if conexao:
                cursor = conexao.cursor()
                try:
                    for item in item_selecionado:
                        valores = self.treeview.item(item, "values")
                        id_fornecedor = valores[0]

                        query = "DELETE FROM fornecedor WHERE ID_Fornecedor = %s"
                        cursor.execute(query, (id_fornecedor,))

                        self.treeview.delete(item)

                    conexao.commit()
                    messagebox.showinfo("Sucesso", "Fornecedor excluído com sucesso.")

                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao excluir fornecedor: {e}")
                finally:
                    conexao.close()
            else:
                messagebox.showerror("Erro", "Erro ao conectar ao banco de dados.")

    def carregar_campus(self, listbox):
        listbox.delete(0, tk.END)
        try:
            conexao = self.conexao_db()
            if conexao:
                cursor = conexao.cursor()
                query = "SELECT Nome_Campus FROM campus"
                cursor.execute(query)
                campus = cursor.fetchall()

                if campus:
                    for campus_item in campus:
                        listbox.insert(tk.END, campus_item[0])
                else:
                    messagebox.showinfo("Aviso", "Nenhum campus encontrado.")

                conexao.close()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar campus disponíveis: {e}")

    def adicionar_fornecedor(self):
        self.limpar_conteudo()

        tk.Label(self.frame_conteudo, text="Adicionar Fornecedor:", font=self.fonte_subtitulo).grid(row=0, column=1, pady=10)
        tk.Label(self.frame_conteudo, text="Nome do Fornecedor", font=self.fonte_texto).grid(row=1, column=0, padx=10, pady=10)
        nome_entry = tk.Entry(self.frame_conteudo, font=self.fonte_texto)
        nome_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.frame_conteudo, text="Contato", font=self.fonte_texto).grid(row=2, column=0, padx=10, pady=10)
        contato_entry = tk.Entry(self.frame_conteudo, font=self.fonte_texto)
        contato_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.frame_conteudo, text="Campus Relacionados:", font=self.fonte_texto).grid(row=3, column=0, padx=10, pady=10)
        campus_listbox = tk.Listbox(self.frame_conteudo, selectmode=tk.MULTIPLE, height=5)
        campus_listbox.grid(row=3, column=1, padx=10, pady=10)
        self.carregar_campus(campus_listbox)

        tk.Label(self.frame_conteudo, text="Região Atendida", font=self.fonte_texto).grid(row=4, column=0, padx=10, pady=10)
        regiao_entry = tk.Entry(self.frame_conteudo, font=self.fonte_texto)
        regiao_entry.grid(row=4, column=1, padx=10, pady=10)

        tk.Label(self.frame_conteudo, text="Data do Contrato", font=self.fonte_texto).grid(row=5, column=0, padx=10, pady=10)
        data_contrato_entry = tk.Entry(self.frame_conteudo, font=self.fonte_texto)
        data_contrato_entry.grid(row=5, column=1, padx=10, pady=10)

        def salvar_fornecedor():
            nome = nome_entry.get()
            contato = contato_entry.get()

            if not nome or not contato:
                messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")
                return
            
            campus_selecionados = [campus_listbox.get(i) for i in campus_listbox.curselection()]
            if not campus_selecionados:
                messagebox.showwarning("Atenção", "Selecione ao menos um campus.")
                return
            
            regiao = regiao_entry.get()
            data_contrato = data_contrato_entry.get()

            try:
                data_contrato_formatada = datetime.strptime(data_contrato, '%d-%m-%y').strftime('%Y-%m-%d')
            except ValueError:
                messagebox.showwarning("Atenção", "Data do contrato deve estar no formato dd-mm-yy.")
                return

            if not regiao or not data_contrato:
                messagebox.showwarning("Atenção", "Região Atendida e Data do Contrato são obrigatórios.")
                return
            
            conexao = self.conexao_db()
            if conexao:
                cursor = conexao.cursor()
                try:
                    query = "INSERT INTO fornecedor (Nome_Fornecedor, Contato) VALUES (%s, %s)"
                    cursor.execute(query, (nome, contato))
                    fornecedor_id = cursor.lastrowid

                    for campus_nome in campus_selecionados:
                        cursor.execute("SELECT ID_Campus FROM campus WHERE Nome_Campus = ?", (campus_nome,))
                        campus_id = cursor.fetchone()[0]

                        query = """
                            INSERT INTO fornecedor_campus (ID_Fornecedor, ID_Campus, Regiao_Atendida, Data_Contrato)
                            VALUES (%s, %s, %s, %s)
                        """
                        cursor.execute(query, (fornecedor_id, campus_id, regiao, data_contrato_formatada))

                    conexao.commit()
                    messagebox.showinfo("Sucesso", "Fornecedor adicionado com sucesso.")
                    self.visualizar_fornecedores()
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao adicionar fornecedor: {e}")
                finally:
                    conexao.close()
            else:
                messagebox.showerror("Erro", "Erro ao conectar ao banco de dados.")

        tk.Button(self.frame_conteudo, text="Salvar", command=salvar_fornecedor, font=self.fonte_pequena).grid(row=6, column=0, columnspan=2, pady=10)

    def editar_fornecedor(self):
        item_selecionado = self.treeview.selection()

        if not item_selecionado:
            messagebox.showwarning("Atenção", "Nenhum fornecedor selecionado para edição.")
            return

        valores = self.treeview.item(item_selecionado[0], "values")
        id_fornecedor = valores[0]
        nome_fornecedor = valores[1]
        contato_fornecedor = valores[2]

        editar_window = tk.Toplevel(self.root)
        editar_window.title("Editar Fornecedor")

        tk.Label(editar_window, text="Nome do Fornecedor:").grid(row=0, column=0, padx=10, pady=5)
        nome_entry = tk.Entry(editar_window)
        nome_entry.insert(0, nome_fornecedor)
        nome_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(editar_window, text="Contato:").grid(row=1, column=0, padx=10, pady=5)
        contato_entry = tk.Entry(editar_window)
        contato_entry.insert(0, contato_fornecedor)
        contato_entry.grid(row=1, column=1, padx=10, pady=5)

        def salvar_edicao():
            novo_nome = nome_entry.get()
            novo_contato = contato_entry.get()

            if not novo_nome or not novo_contato:
                messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")
                return

            conexao = self.conexao_db()
            if conexao:
                cursor = conexao.cursor()
                try:
                    query = "UPDATE fornecedor SET Nome_Fornecedor = %s, Contato = %s WHERE ID_Fornecedor = %s"
                    cursor.execute(query, (novo_nome, novo_contato, id_fornecedor))
                    conexao.commit()
                    messagebox.showinfo("Sucesso", "Fornecedor atualizado com sucesso.")

                    self.treeview.item(item_selecionado[0], values=(id_fornecedor, novo_nome, novo_contato))

                    editar_window.destroy()

                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao atualizar fornecedor: {e}")
                finally:
                    conexao.close()
            else:
                messagebox.showerror("Erro", "Erro ao conectar ao banco de dados.")

        tk.Button(editar_window, text="Salvar", command=salvar_edicao).grid(row=2, column=0, columnspan=2, pady=10)

    def visualizar_auditoria(self):
        self.limpar_conteudo()

        conexao = self.conexao_db()
        if conexao:
            cursor = conexao.cursor()
            query = "SELECT * FROM auditoria_equipamento"
            cursor.execute(query)
            auditoria = cursor.fetchall()

            for widget in self.frame_conteudo.winfo_children():
                widget.destroy()

            self.treeview = ttk.Treeview(self.frame_conteudo, columns=("ID_Log", "ID_Equipamento", "Status_Antigo", "Status_Novo", "Data_Alteracao"), show="headings")
            self.treeview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            self.treeview.heading("ID_Log", text="ID Log")
            self.treeview.heading("ID_Equipamento", text="ID Equipamento")
            self.treeview.heading("Status_Antigo", text="Status Antigo")
            self.treeview.heading("Status_Novo", text="Status Novo")
            self.treeview.heading("Data_Alteracao", text="Data da Alteração")

            for log in auditoria:
                self.treeview.insert("", "end", values=log)

            for col in self.treeview["columns"]:
                self.treeview.column(col, width=150)

            self.frame_conteudo.grid_rowconfigure(0, weight=1)
            self.frame_conteudo.grid_columnconfigure(0, weight=1)

            tk.Button(self.frame_conteudo, text="Visualizar Equipamentos", command=self.visualizar_equipamentos, font=self.fonte_pequena).grid(row=1, column=0, padx=10, pady=10)

            conexao.close()
        else:
            tk.messagebox.showerror("Erro", "Erro ao conectar ao banco de dados.")

    @staticmethod
    def conexao_db():
        try:
            conexao = mariadb.connect(
                user="root",
                password="root",
                host="localhost",
                port=3306,
                database="inventario"
            )
            return conexao
        except Exception as e:
            print(f"ERRO AO CONECTAR BANCO: {e}")
            return None

conexao = Inventario.conexao_db()
if conexao:
    sql = conexao.cursor()

root = tk.Tk()
app = Inventario(root)
root.mainloop()

if conexao:
    conexao.close()
