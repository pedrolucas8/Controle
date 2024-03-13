class structtype():
    """ Inicialização da variável
        
        >>> A = structtype()
        ou
        >>> A = structtype(a=10,b=20,c=30)
    """
    def __init__(self,**kwargs):
        self.Set(**kwargs)
    
    """ Adicionando novas variáveis

        >>> A.Set(a=10)
        ou
        >>> A.a = 10
    """
    def Set(self,**kwargs):
        self.__dict__.update(kwargs)

    """ Adicionando novas variáveis por string

        >>> lab = 'a'
        >>> val = 10
        >>> AA.SetAttr(lab,val)
    """
    def SetAttr(self,lab,val):
        self.__dict__[lab] = val

    """ Apresenta todos os campos do struct
    """
    def Show(self,Ntabs=0,prefixo=""):
        variaveis = vars(self)
        if Ntabs == 0:
            print("CAMPOS DO STRUCT")
        for nome in variaveis:
            var = variaveis[nome]
            textobase = Ntabs*"  "+f"{prefixo}{nome}"
            if type(var) is not structtype:
                print(textobase+f"\t: {var}")
            else:
                print(textobase+f"   STRUCT")
                var.Show(Ntabs=Ntabs+1,prefixo=".")





if __name__ == "__main__":
    AA = structtype(a=10,b=100.328,c=structtype(a=1000))
    AA.cc = "Hello World!!"
    AA.c.b = -50
    AA.d = structtype(x=0)
    AA.c.c = structtype(a = 10)
    AA.Set(z=10)
    AA.SetAttr("j",30)
    
    AA.Show()