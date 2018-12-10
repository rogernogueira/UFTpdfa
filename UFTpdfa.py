#!c:\Program Files\Python36\python.exe
from tkinter import filedialog
import tkinter as tk
import tkinter.messagebox
import os
from unicodedata import normalize
import getpass

def tratarNome(nomearquivo):
    aux=nomearquivo
    nomearquivo=nomearquivo.replace(' ', '_') # retira espaços dos nomes
    nomearquivo=normalize('NFKD', nomearquivo).encode('ASCII', 'ignore').decode('ASCII') # retira os caracteres especiais
    os.rename(aux, nomearquivo)# renomeia arquivo
    return nomearquivo

def interface():
    label=tk.Label(frame,text="Escolha uma opção de conversão para PDF/A: ")
    label.grid(column=0, row=0, columnspan=2, pady=5)
    btArquivo = tk.Button(frame,
                       text="Arquivo",
                       fg="red",
                       command=selectArquivo,
                       width= "10",
                       height="3"
                       )
    btArquivo.grid(column=0, row=1, pady=5)
    btDiretorio = tk.Button(frame,
                       text="Pasta",
                       width= "10",
                       height="3",

                       command=selectDiretorio)
    btDiretorio.grid(column=1,row=1, pady=5)
    lbPasta=tk.Label(frame,text="Pasta padrão: ")
    lbPasta.grid(column=0, row=2, sticky=tk.E)
    editPasta.grid(column=1, row=2, sticky=tk.W, pady=5)
    root.mainloop()


def selectArquivo():
    nomeArquivo= filedialog.askopenfilename(initialdir = "/users/"+getpass.getuser()+"/Desktop",title = "Escolha um arquivo",filetypes = (("Arquivos PDF","*.pdf"),("all files","*.*")))
   # nomeArquivo =  filedialog.askopenfilename(initialdir = "/users/"+getpass.getuser()+"/Desktop",title = "Selecione o arquivo", filetypes = (("jpeg files","*.jpg")))
    if nomeArquivo=='':
        return
    if nomeArquivo[-4:] !='.pdf':
        tk.messagebox.showinfo("Aviso", "Não é arquivo pdf.")
        return
    os.chdir(os.path.dirname(nomeArquivo))
    dirTrabalho=(os.getcwd())
    tk.messagebox.showinfo("Aviso", "Selecione a pasta onde vai ficar o Arquivo PDF/A")
    diretorio=  filedialog.askdirectory(initialdir = "/users/"+getpass.getuser()+"/Desktop",title = "Selecione o Diretorio",)
    if os.path.isfile(diretorio+'/'+os.path.basename(nomeArquivo)):
        tk.messagebox.showinfo("Aviso", "Já existe um arquivo com este nome na pasta {}.".format(diretorio))
        return
    log_ok=[]
    log_erro=[]
    try:
        print(diretorio+'/'+os.path.basename(nomeArquivo))
        os.system( 'gswin64 -dPDFA=1   -dBATCH  -sColorConversionStrategy=/RGB  -dNOPAUSE -sDEVICE=pdfwrite -dUseCIEColor -sOutputFile="%s"  "%s"  ' % (diretorio+'/'+os.path.basename(nomeArquivo),nomeArquivo))
        log_ok.append(nomeArquivo)

    except:
        print('O arquivo {} não pode ser convertido em PDFA.'.format(nomeArquivo))
        log_erro.append(nomeArquivo)
    if len(log_erro)!=0:
        tk.messagebox.showinfo("Aviso", 'Alguns arquivos não foram convertidos: '+str(log_erro))
    else:
        tk.messagebox.showinfo("Aviso", 'Arquivo covertido com sucesso.')


def selectDiretorio():
    pastaPadrao=editPasta.get()
    diretorio=  filedialog.askdirectory(initialdir = "/users/"+getpass.getuser()+"/Desktop",title = "Selecione a Pasta")
    if diretorio=='':
        return
    cont=0
    for f in os.listdir(diretorio):
        if f[-4:] =='.pdf':
            cont+=1
    if cont==0:
        tk.messagebox.showinfo("Aviso", "Não há arquivos pdf nesta pasta.")
        return

    os.chdir(diretorio)
    log_ok=[]
    log_erro=[]
    arquivos = os.listdir(diretorio) # lista arquivos do diretorio
    if os.path.isdir('./'+pastaPadrao): # checa se pasta já existe
        tk.messagebox.showinfo("Aviso", 'Pasta Padrão  já existente, caso queria continuar delete ou renomei a pasta {} e tente novamente.'.format(pastaPadrao))
        return
        #print('Pasta "pdfa" já existente, caso queria continuar delete ou renomei a pasta pdfa e tente novamente.')

    else:
        os.mkdir('./'+pastaPadrao,mode=0o777) # se pasta não existe cria pasta pdfa
    for f in arquivos:
        if f[-4:] =='.pdf':
            f=tratarNome(f)
            try:
                os.system( 'gswin64 -dPDFA=1   -dBATCH  -sColorConversionStrategy=/RGB  -dNOPAUSE -sDEVICE=pdfwrite -dUseCIEColor -sOutputFile="%s"  "%s"  ' % (pastaPadrao+'//'+f,f))
                log_ok.append(f)
            except:
                print('O arquivo {} não pode ser convertido em PDFA.'.format(f))
                log_erro.append(f)
    if len(log_erro)==0 and len(log_ok)==0:
        print('Nenhum arquivo PDF foi encontrado.')
        os.remove('./pdfa')
    if len(log_erro)==0:
        tk.messagebox.showinfo("Aviso", 'Todos os arquivos foram convertidos com SUCESSO...')
        #print('Todos os arquivos foram convertidos com SUCESSO...')
    else:
        tk.messagebox.showinfo("Aviso", 'Alguns arquivos não foram convertidos: '+str(log_erro))
        #print('Arquivos não covertidos: ')
        #print(str(log_erro))

root = tk.Tk()
root.title("UFT - Conversor PDF/A")
root.resizable(False, False)
#Largura x Altura + Esquerda do video + Top do video
root.geometry("295x150+100+100")
frame = tk.Frame(root, bd=1, relief=tk.SUNKEN)
frame.grid(column=0, row=0, pady=10, padx=10)
editPasta= tk.Entry(frame, width="18")
editPasta.insert(10,'PDFA')

interface()

exit()



