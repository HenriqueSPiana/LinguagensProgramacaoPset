# IDENTIFICAÇÃO DO ESTUDANTE:
# Preencha seus dados e leia a declaração de honestidade abaixo. NÃO APAGUE
# nenhuma linha deste comentário de seu código!
#
#    Nome completo:Henrique Schrock Piana
#    Matrícula:202202403
#    Turma:CC6N
#    Email:h.spiana80@gmail.com
#
# DECLARAÇÃO DE HONESTIDADE ACADÊMICA:
# Eu afirmo que o código abaixo foi de minha autoria. Também afirmo que não
# pratiquei nenhuma forma de "cola" ou "plágio" na elaboração do programa,
# e que não violei nenhuma das normas de integridade acadêmica da disciplina.
# Estou ciente de que todo código enviado será verificado automaticamente
# contra plágio e que caso eu tenha praticado qualquer atividade proibida
# conforme as normas da disciplina, estou sujeito à penalidades conforme
# definidas pelo professor da disciplina e/ou instituição.


# Imports permitidos (não utilize nenhum outro import!):
import sys
import math
import base64
import tkinter
from io import BytesIO

from PIL import Image as PILImage



class kernel:
    """
    Criado uma classe kernel, para facilitar a manipulacao e codificacao das funcoes assim como o entendimento do codigo
    """

    def __init__(self, largura, altura, pixels):

        """
        atributos da classe kernel é igual ao de imagem, pois ele vai ser usado como forma de matriz para multiplicacao. 
        """
        self.largura = largura
        self.altura = altura
        self.pixels = pixels 


    
    def get_pixel(self,x,y):
        """
        Metodo tratado para converter parametro x,y bidimensional de cordenadas cartesianas, para indice em array
        """
        return self.pixels[(y * self.largura) + x]
    
    def n_por_n(n):
        """
        Metodo que calcula a matriz de blur, que para aplicar precisa que a soma de todos os itens da matriz seja 1
        """
        k = []
        for i in range(n):
            for j in range(n):
                k.append(1/n**2) 
                # 1 pelo quadrado de N pq é o numero total de itens na lista, e com isso a soma de todos da 1, que é o necessario para esse blur
        return k

    def get_meio(self):
        """
        Metodo que pega o meio do kernel, para que seja feito os calculos 
        precisa saber qual posição do kernel deve ser alinhada com o pixel atual. Por convenção, usa-se o centro do kernel como ponto de referência.
        """
        meioX = self.largura//2
        meioY = self.altura//2
        return (meioX,meioY)



# Classe Imagem:
class Imagem:
    def __init__(self, largura, altura, pixels):
        self.largura = largura
        self.altura = altura
        self.pixels = pixels #row-major order

    def get_pixel(self,x,y):
        """
        Metodo que pega o pixel com base no x,y passados, por ser na imagem ele tem um tratamento de limite para que seja possivel usar a correlacao
        """
        #y = linha
        #x = coluna

        limiteHorizontal = self.largura-1
        limiteVertical= self.altura-1
        if (x<0):
            x=0
        elif (x > (limiteHorizontal)):
            x = limiteHorizontal
        if (y<0):
            y=0
        elif(y>limiteVertical):
            y=limiteVertical

        #converter parametro x,y bidimensional de cordenadas cartesianas, para indice em array
        return self.pixels[(y * self.largura) + x]


    def set_pixel(self,x,y,c):
        #para que eu consiga acessar realmente os pixels corretos, é preciso pular os pixels de acordo com a largura.
        # se está na linha 0 entao é vindo o valor da coluna somente
        self.pixels[(y * self.largura) + x] = c

        
    def aplicar_por_pixel(self, func):
        """
        Metodo aplica com base em uma funcao passada, valor novo de um pixel.
        """
        # foi necessario ajustes para que percorresse o vetor de forma correta
        resultado = Imagem.nova(self.largura,self.altura)
        for x in range(resultado.largura):
            for y in range(resultado.altura):
                cor = self.get_pixel(x,y)
                nova_cor = func(cor)
                resultado.set_pixel(x,y, nova_cor)
        return resultado
    

    def aplicar_por_coordenada(self, func):
        """
        Metodo que utiliza a coordenada x,y para aplicar a funcao, 
        para quando a funcao utiliza a coordenada, e nao o indice/valor atual do pixel
        """
        resultado = Imagem.nova(self.largura, self.altura)
        for x in range(resultado.largura):
            for y in range(resultado.altura):
                novo_pixel = func(x, y)
                resultado.set_pixel(x, y, novo_pixel)
        return resultado
    

    def invertida(self):
        return self.aplicar_por_pixel(lambda c: 255 - c)


    def tramontinaCorteRapido(self):

        """
        Metodo que separa o tratamento de capagem dos pixels da correlacao.
        sendo usado somente no final das funcoes e nao na correlacao em si pois caso usado na correlacao os dados sao sujados pelo 
        arredondamento e truncamento.
        """
        #tratamento para corte de pixels, se extender dos valores suportados, o pixel é capado
        for x in range(self.largura):
            for y in range(self.altura):
                pixelAtual = self.get_pixel(x, y)
                if pixelAtual < 0:
                    self.set_pixel(x, y, 0)
                elif pixelAtual > 255:
                    self.set_pixel(x, y, 255)
                else:
                    self.set_pixel(x, y, round(pixelAtual))
        return self
        


    def correlacao(self, kernel):
        """ Metodo aplica a correlacao pegando o pixel central do kernel e alinhando com o pixel que será aplicado."""
        resultado = Imagem.nova(self.largura, self.altura)
        DistanciaDoCentroX, DistanciaDoCentroY = kernel.get_meio()
                        #Calcula o centro do kernel (por exemplo, para kernel 3x3, seria (1,1))
                #usado para centralizar o kernel sobre cada pixel que está processando

        for x in range(resultado.largura):
            for y in range(resultado.altura):
                correlacao = 0          #acumulador para calcular novo valor do pixel        
                # Percorrem cada pixel da imagem original
                # Cada (x,y) é o pixel central onde vamos aplicar o kernel
                
                for i in range(kernel.largura):
                    for j in range(kernel.altura):
                        #Percorrem cada posição do kernel
                        # Para cada posição, calculamos qual pixel da imagem original corresponde a esta posição do kernel
                        x1 = x - DistanciaDoCentroX + i
                        y1 = y - DistanciaDoCentroY + j
                        correlacao += self.get_pixel(x1, y1) * kernel.get_pixel(i, j)

                # Define o valor de correlacao após o cálculo completo para (x, y)
                resultado.set_pixel(x, y, correlacao)
        
        return resultado

        
    def borrada(self, n):
        #  instancia um kernel de tamanho nxn e uma matriz nxn que a some é igual a 1
        kern = kernel(n,n,kernel.n_por_n(n))
        resultado = self.correlacao(kern)
        #aplica e depois trata limites
        return resultado.tramontinaCorteRapido()



    def focada(self, n):

        resultado = self.nova(self.largura,self.altura)
        naoFocada = self.borrada(n)
        #instancia uma imagem borrada para melhoria de definicao
        for x in range(resultado.largura):
            for y in range(resultado.altura):
                #aplica a formula fornecida, para melhorar a imagem. 
                # que é subtração de uma versão embaçada da imagem de uma versão em escala da imagem original.
                novoPixel = 2*self.get_pixel(x,y) - naoFocada.get_pixel(x,y)
                resultado.set_pixel(x,y,novoPixel)
        return resultado.tramontinaCorteRapido()

    def bordas(self):
        """Esse método aplica uma detecção de bordas em uma imagem usando dois kernels (um para a direção horizontal e outro para a vertical) 
        e,depois combina os resultados para encontrar a borda em cada pixel"""
        resultado = Imagem.nova(self.largura, self.altura)

        kernel_x =kernel(3,3,[-1, 0, 1,-2, 0, 2,-1, 0, 1]) #usado para calcular as mudanças na direção horizontal.
        kernel_y =kernel(3,3,[-1, -2, -1,0, 0, 0,1, 2, 1]) #usado para calcular as mudanças na direção vertical.

        imagem_x = self.correlacao(kernel_x) #aplica o kernel na imagem passada e copia para a imagem x e y
        imagem_y = self.correlacao(kernel_y) 

        resultado = self.aplicar_por_coordenada(
        lambda  x, y: math.sqrt(imagem_x.get_pixel(x, y) ** 2 + imagem_y.get_pixel(x, y) ** 2))
        #função calcula o tamanho da borda para cada pixel juntando imagem_x e imagem_y:
        
        resultado = resultado.tramontinaCorteRapido()
        return resultado


    # Abaixo deste ponto estão utilitários para carregar, salvar e mostrar
    # as imagens, bem como para a realização de testes. Você deve ler as funções
    # abaixo para entendê-las e verificar como funcionam, mas você não deve
    # alterar nada abaixo deste comentário.
    #
    # ATENÇÃO: NÃO ALTERE NADA A PARTIR DESTE PONTO!!! Você pode, no final
    # deste arquivo, acrescentar códigos dentro da condicional
    #
    #                 if __name__ == '__main__'
    #
    # para executar testes e experiências enquanto você estiver executando o
    # arquivo diretamente, mas que não serão executados quando este arquivo
    # for importado pela suíte de teste e avaliação.
    def __eq__(self, other):
        return all(getattr(self, i) == getattr(other, i)
                   for i in ('altura', 'largura', 'pixels'))

    def __repr__(self):
        return "Imagem(%s, %s, %s)" % (self.largura, self.altura, self.pixels)

    @classmethod
    def carregar(cls, nome_arquivo):
        """
        Carrega uma imagem do arquivo fornecido e retorna uma instância dessa
        classe representando essa imagem. Também realiza a conversão para tons
        de cinza.

        Invocado como, por exemplo:
           i = Imagem.carregar('test_images/cat.png')
        """
        with open(nome_arquivo, 'rb') as guia_para_imagem:
            img = PILImage.open(guia_para_imagem)
            img_data = img.getdata()
            if img.mode.startswith('RGB'):
                pixels = [round(.299 * p[0] + .587 * p[1] + .114 * p[2]) for p in img_data]
            elif img.mode == 'LA':
                pixels = [p[0] for p in img_data]
            elif img.mode == 'L':
                pixels = list(img_data)
            else:
                raise ValueError('Modo de imagem não suportado: %r' % img.mode)
            l, a = img.size
            return cls(l, a, pixels)

    @classmethod
    def nova(cls, largura, altura):
        """
        Cria imagens em branco (tudo 0) com a altura e largura fornecidas.

        Invocado como, por exemplo:
            i = Imagem.nova(640, 480)
        """
        return cls(largura, altura, [0 for i in range(largura * altura)])

    def salvar(self, nome_arquivo, modo='PNG'):
        """
        Salva a imagem fornecida no disco ou em um objeto semelhante a um arquivo.
        Se o nome_arquivo for fornecido como uma string, o tipo de arquivo será
        inferido a partir do nome fornecido. Se nome_arquivo for fornecido como
        um objeto semelhante a um arquivo, o tipo de arquivo será determinado
        pelo parâmetro 'modo'.
        """
        saida = PILImage.new(mode='L', size=(self.largura, self.altura))
        saida.putdata(self.pixels)
        if isinstance(nome_arquivo, str):
            saida.save(nome_arquivo)
        else:
            saida.save(nome_arquivo, modo)
        saida.close()

    def gif_data(self):
        """
        Retorna uma string codificada em base 64, contendo a imagem
        fornecida, como uma imagem GIF.

        Função utilitária para tornar show_image um pouco mais limpo.
        """
        buffer = BytesIO()
        self.salvar(buffer, modo='GIF')
        return base64.b64encode(buffer.getvalue())

    def mostrar(self):
        """
        Mostra uma imagem em uma nova janela Tk.
        """
        global WINDOWS_OPENED
        if tk_root is None:
            # Se Tk não foi inicializado corretamente, não faz mais nada.
            return
        WINDOWS_OPENED = True
        toplevel = tkinter.Toplevel()
        # O highlightthickness=0 é um hack para evitar que o redimensionamento da janela
        # dispare outro evento de redimensionamento (causando um loop infinito de
        # redimensionamento). Para maiores informações, ver:
        # https://stackoverflow.com/questions/22838255/tkinter-canvas-resizing-automatically
        tela = tkinter.Canvas(toplevel, height=self.altura,
                              width=self.largura, highlightthickness=0)
        tela.pack()
        tela.img = tkinter.PhotoImage(data=self.gif_data())
        tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        def ao_redimensionar(event):
            # Lida com o redimensionamento da imagem quando a tela é redimensionada.
            # O procedimento é:
            #  * converter para uma imagem PIL
            #  * redimensionar aquela imagem
            #  * obter os dados GIF codificados em base 64 (base64-encoded GIF data)
            #    a partir da imagem redimensionada
            #  * colocar isso em um label tkinter
            #  * mostrar a imagem na tela
            nova_imagem = PILImage.new(mode='L', size=(self.largura, self.altura))
            nova_imagem.putdata(self.pixels)
            nova_imagem = nova_imagem.resize((event.width, event.height), PILImage.NEAREST)
            buffer = BytesIO()
            nova_imagem.save(buffer, 'GIF')
            tela.img = tkinter.PhotoImage(data=base64.b64encode(buffer.getvalue()))
            tela.configure(height=event.height, width=event.width)
            tela.create_image(0, 0, image=tela.img, anchor=tkinter.NW)

        # Por fim, faz o bind da função para que ela seja chamada quando a tela
        # for redimensionada:
        tela.bind('<Configure>', ao_redimensionar)
        toplevel.bind('<Configure>', lambda e: tela.configure(height=e.height, width=e.width))

        # Quando a tela é fechada, o programa deve parar
        toplevel.protocol('WM_DELETE_WINDOW', tk_root.destroy)


# Não altere o comentário abaixo:
# noinspection PyBroadException
try:
    tk_root = tkinter.Tk()
    tk_root.withdraw()
    tcl = tkinter.Tcl()


    def refaz_apos():
        tcl.after(500, refaz_apos)


    tcl.after(500, refaz_apos)
except:
    tk_root = None

WINDOWS_OPENED = False

if __name__ == '__main__':
    # O código neste bloco só será executado quando você executar
    # explicitamente seu script e não quando os testes estiverem
    # sendo executados. Este é um bom lugar para gerar imagens, etc.

    # Diretório



    im = Imagem.carregar(nome_arquivo='test_images/construct.png')
    borda = im.bordas() 
    borda.salvar('resultados/construct_borda.png')






    # im = Imagem.carregar(nome_arquivo='test_images/python.png')
    # focada = im.focada(11) 
    # focada.salvar('resultados/python_focado.png')






    # im = Imagem.carregar(nome_arquivo='test_images/cat.png')
    # desfoque = im.borrada(5) 
    # desfoque.salvar('resultados/cat_desfoque.png')



    # kn = kernel(9,9,[0, 0, 0, 0, 0, 0, 0, 0, 0,
    #                 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #                 1, 0, 0, 0, 0, 0, 0, 0, 0,
    #                 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #                 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #                 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #                 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #                 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #                 0, 0, 0, 0, 0, 0, 0, 0, 0])
    
    # im = Imagem.carregar(nome_arquivo='test_images/pigbird.png')
    # correlacao = im.correlacao(kn) 
    # correlacao.salvar('resultados/pigbird_correlacao.png')




    
    # im = Imagem.carregar(nome_arquivo='test_images/bluegill.png')
    # invertida = im.invertida() 
    # invertida.salvar('resultados/bluegill_invertida.png')
                         
    # pass
    # O código a seguir fará com que as janelas de Imagem.mostrar
    # sejam exibidas corretamente, quer estejamos executando
    # interativamente ou não:
    if WINDOWS_OPENED and not sys.flags.interactive:
        tk_root.mainloop()
