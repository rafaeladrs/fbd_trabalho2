from functools import partial
import tkinter as tk
from tkinter import ttk, messagebox
import mariadb

class Inventario:
    def __init__(self, root):
        self.root = root
        self.root.title("Inventário IF")
        self.root.geometry("850x600")
        self.root.resizable(False, False)

        self.fonte_texto = ("Arial", 10)
        self.fonte_titulo = ("Arial", 14, "bold")
        self.fonte_subtitulo = ("Arial", 12, "bold")
        self.fonte_pequena = ("Arial", 8)
        
        # Título
        tk.Label(self.root, text="Inventário do IF", font=self.fonte_titulo).grid(row=0, column=1, columnspan=2, pady=10)
        
        tk.Button(self.root, text="Adicionar Equipamento", command=self.adicionar_equipamento, font=self.fonte_pequena).grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        tk.Button(self.root, text="Visualizar Equipamentos", command=self.visualizar_equipamentos, font=self.fonte_pequena).grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        tk.Button(self.root, text="Adicionar Setor", command=self.adicionar_setor, font=self.fonte_pequena).grid(row=1, column=2, padx=10, pady=10, sticky="ew")
        tk.Button(self.root, text="Visualizar Setores", command=self.visualizar_setores, font=self.fonte_pequena).grid(row=1, column=3, padx=10, pady=10, sticky="ew")
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

        tk.Label(self.frame_conteudo, text="Valor de Aquisição (R$):", font=self.fonte_texto).grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.f_valor_aquisicao = tk.Entry(self.frame_conteudo, width=30)
        self.f_valor_aquisicao.grid(row=4, column=1, padx=10, pady=10)

        tk.Label(self.frame_conteudo, text="Valor Depreciado (R$):", font=self.fonte_texto).grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.f_valor_depreciado = tk.Entry(self.frame_conteudo, width=30)
        self.f_valor_depreciado.grid(row=5, column=1, padx=10, pady=10)

        tk.Label(self.frame_conteudo, text="Número da Nota Fiscal:", font=self.fonte_texto).grid(row=6, column=0, padx=10, pady=10, sticky="w")
        self.f_numero_nota_fiscal = tk.Entry(self.frame_conteudo, width=30)
        self.f_numero_nota_fiscal.grid(row=6, column=1, padx=10, pady=10)

        tk.Label(self.frame_conteudo, text="Número de Série:", font=self.fonte_texto).grid(row=7, column=0, padx=10, pady=10, sticky="w")
        self.f_numero_serie = tk.Entry(self.frame_conteudo, width=30)
        self.f_numero_serie.grid(row=7, column=1, padx=10, pady=10)

        tk.Button(self.frame_conteudo, text="Registrar", command=self.registrar_equipamento, font=self.fonte_subtitulo).grid(row=8, column=1, pady=20)

    def registrar_equipamento(self):
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
            tk.messagebox.showerror("Erro", f"Erro ao inserir no banco: {e}")

    def visualizar_equipamentos(self):
        self.limpar_conteudo()

        conexao = self.conexao_db()
        if conexao:
            cursor = conexao.cursor()
            query = "SELECT * FROM equipamento"
            cursor.execute(query)
            equipamentos = cursor.fetchall()

            for widget in self.frame_conteudo.winfo_children():
                widget.destroy()

            self.treeview = ttk.Treeview(self.frame_conteudo, columns=("ID", "Descrição", "Status", "Estado", "Valor Aquisição", "Valor Depreciado", "Número Nota Fiscal", "Número Série"), show="headings")
            self.treeview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            self.treeview.heading("ID", text="ID")
            self.treeview.heading("Descrição", text="Descrição")
            self.treeview.heading("Status", text="Status")
            self.treeview.heading("Estado", text="Estado de Conservação")
            self.treeview.heading("Valor Aquisição", text="Valor Aquisição")
            self.treeview.heading("Valor Depreciado", text="Valor Depreciado")
            self.treeview.heading("Número Nota Fiscal", text="Número Nota Fiscal")
            self.treeview.heading("Número Série", text="Número Série")

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

    def adicionar_setor(self):
        self.limpar_conteudo()

        tk.Label(self.frame_conteudo, text="Adicionar Setor:", font=self.fonte_subtitulo).grid(row=0, column=1, pady=10)

        tk.Label(self.frame_conteudo, text="Nome do Setor:", font=self.fonte_texto).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.f_nome_setor = tk.Entry(self.frame_conteudo, width=30)
        self.f_nome_setor.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.frame_conteudo, text="Responsável:", font=self.fonte_texto).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.f_responsavel = tk.Entry(self.frame_conteudo, width=30)
        self.f_responsavel.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self.frame_conteudo, text="Registrar", command=self.registrar_setor, font=self.fonte_subtitulo).grid(row=3, column=1, padx=10, pady=10)

    def registrar_setor(self):
        nome_setor = self.f_nome_setor.get()
        responsavel = self.f_responsavel.get()

        if not nome_setor or not responsavel:
            tk.messagebox.showerror("Erro", "Por favor, preencha todos os campos obrigatórios.")
            return

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
                tk.messagebox.showinfo("Sucesso", "Setor registrado com sucesso!")
                conexao.close()
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

        def salvar_edicao():
            novo_nome = nome_entry.get()
            novo_responsavel = responsavel_entry.get()

            if not novo_nome or not novo_responsavel:
                messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")
                return

            conexao = self.conexao_db()
            if conexao:
                cursor = conexao.cursor()
                try:
                    query = "UPDATE setor SET Nome_Setor = %s, Responsavel = %s WHERE ID_Setor = %s"
                    cursor.execute(query, (novo_nome, novo_responsavel, id_setor))
                    conexao.commit()

                    self.treeview.item(item_selecionado[0], values=(id_setor, novo_nome, novo_responsavel))

                    messagebox.showinfo("Sucesso", "Setor atualizado com sucesso.")
                    editar_window.destroy()

                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao atualizar setor: {e}")
                finally:
                    conexao.close()

        tk.Button(editar_window, text="Salvar", command=salvar_edicao).grid(row=2, column=0, columnspan=2, pady=10)

    def adicionar_campus(self):
        self.limpar_conteudo()

        tk.Label(self.frame_conteudo, text="Adicionar Campus:", font=self.fonte_subtitulo).grid(row=0, column=1, pady=10)
        tk.Label(self.frame_conteudo, text="Nome do Campus", font=self.fonte_texto).grid(row=1, column=0, padx=10, pady=10)
        nome_entry = tk.Entry(self.frame_conteudo, font=self.fonte_texto)
        nome_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.frame_conteudo, text="Endereço", font=self.fonte_texto).grid(row=2, column=0, padx=10, pady=10)
        endereco_entry = tk.Entry(self.frame_conteudo, font=self.fonte_texto)
        endereco_entry.grid(row=2, column=1, padx=10, pady=10)

        def salvar_campus():
            nome = nome_entry.get()
            endereco = endereco_entry.get()

            if not nome or not endereco:
                messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")
                return

            conexao = self.conexao_db()
            if conexao:
                cursor = conexao.cursor()
                try:
                    query = "INSERT INTO campus (Nome_Campus, Endereco) VALUES (%s, %s)"
                    cursor.execute(query, (nome, endereco))
                    conexao.commit()
                    messagebox.showinfo("Sucesso", "Campus adicionado com sucesso.")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao adicionar campus: {e}")
                finally:
                    conexao.close()
            else:
                messagebox.showerror("Erro", "Erro ao conectar ao banco de dados.")

        tk.Button(self.frame_conteudo, text="Salvar", command=salvar_campus, font=self.fonte_pequena).grid(row=3, column=0, columnspan=2, pady=10)

    def visualizar_campus(self):
        self.limpar_conteudo()

        conexao = self.conexao_db()
        if conexao:
            cursor = conexao.cursor()
            query = "SELECT * FROM campus"
            cursor.execute(query)
            campus = cursor.fetchall()

            for widget in self.frame_conteudo.winfo_children():
                widget.destroy()

            self.treeview = ttk.Treeview(self.frame_conteudo, columns=("ID", "Nome", "Endereço"), show="headings")
            self.treeview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            self.treeview.heading("ID", text="ID")
            self.treeview.heading("Nome", text="Nome do Campus")
            self.treeview.heading("Endereço", text="Endereço")

            for col in self.treeview["columns"]:
                self.treeview.column(col, width=150)

            for item in campus:
                self.treeview.insert("", "end", values=item)

            self.frame_conteudo.grid_rowconfigure(0, weight=1)
            self.frame_conteudo.grid_columnconfigure(0, weight=1)

            tk.Button(self.frame_conteudo, text="Excluir Campus", command=self.excluir_campus, font=self.fonte_pequena).grid(row=1, column=0, padx=10, pady=10)
            tk.Button(self.frame_conteudo, text="Excluir em Massa", command=lambda: self.excluir_em_massa("campus"), font=self.fonte_pequena).grid(row=2, column=0, padx=10, pady=10)
            tk.Button(self.frame_conteudo, text="Adicionar Campus", command=self.adicionar_campus, font=self.fonte_pequena).grid(row=3, column=0, padx=10, pady=10)
            tk.Button(self.frame_conteudo, text="Editar Campus", command=self.editar_campus, font=self.fonte_pequena).grid(row=4, column=0, padx=10, pady=10)


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
            query = "SELECT * FROM fornecedor"
            cursor.execute(query)
            fornecedores = cursor.fetchall()

            for widget in self.frame_conteudo.winfo_children():
                widget.destroy()

            self.treeview = ttk.Treeview(self.frame_conteudo, columns=("ID", "Nome", "Contato"), show="headings")
            self.treeview.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

            self.treeview.heading("ID", text="ID")
            self.treeview.heading("Nome", text="Nome do Fornecedor")
            self.treeview.heading("Contato", text="Contato")

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

    def adicionar_fornecedor(self):
        self.limpar_conteudo()

        tk.Label(self.frame_conteudo, text="Adicionar Fornecedor:", font=self.fonte_subtitulo).grid(row=0, column=1, pady=10)
        tk.Label(self.frame_conteudo, text="Nome do Fornecedor", font=self.fonte_texto).grid(row=1, column=0, padx=10, pady=10)
        nome_entry = tk.Entry(self.frame_conteudo, font=self.fonte_texto)
        nome_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.frame_conteudo, text="Contato", font=self.fonte_texto).grid(row=2, column=0, padx=10, pady=10)
        contato_entry = tk.Entry(self.frame_conteudo, font=self.fonte_texto)
        contato_entry.grid(row=2, column=1, padx=10, pady=10)

        def salvar_fornecedor():
            nome = nome_entry.get()
            contato = contato_entry.get()

            if not nome or not contato:
                messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos.")
                return

            conexao = self.conexao_db()
            if conexao:
                cursor = conexao.cursor()
                try:
                    query = "INSERT INTO fornecedor (Nome_Fornecedor, Contato) VALUES (%s, %s)"
                    cursor.execute(query, (nome, contato))
                    conexao.commit()
                    messagebox.showinfo("Sucesso", "Fornecedor adicionado com sucesso.")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao adicionar fornecedor: {e}")
                finally:
                    conexao.close()
            else:
                messagebox.showerror("Erro", "Erro ao conectar ao banco de dados.")

        tk.Button(self.frame_conteudo, text="Salvar", command=salvar_fornecedor, font=self.fonte_pequena).grid(row=3, column=0, columnspan=2, pady=10)

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
