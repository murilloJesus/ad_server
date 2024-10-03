from ldap3 import Server, Connection, ALL, NTLM

class activityDirectoryModel:
    def __init__(self, ad_server, ad_domain):
        self.ad_server = ad_server
        self.ad_domain = ad_domain

    def authenticate(self, username, password):
        """
        Autentica um usuário no Active Directory.
        """
        user = f'{self.ad_domain}\\{username}'

        try:
            # Cria uma conexão com o servidor AD
            server = Server(self.ad_server, get_info=ALL)
            conn = Connection(server, user=user, password=password, authentication=NTLM, auto_bind=True)

            if conn.bind():
                conn.search('dc=seu_dominio,dc=local', '(sAMAccountName=usuario)', attributes=['cn'])

                username = conn.entries[0].cn

                conn.search(
                    search_base=f"DC={self.ad_domain.split('.')[0]},DC={self.ad_domain.split('.')[1]}",  # Base do domínio
                    search_filter=f"(sAMAccountName={username})",  # Filtro pelo nome do usuário
                    search_scope=SUBTREE,
                    attributes=['memberOf']  # Atributo que contém os grupos
                )
                
                # Extrair grupos da resposta
                if conn.entries:
                    user_info = conn.entries[0]
                    groups = user_info.memberOf
                    # Retorna os grupos como uma lista simples de strings
                    return {
                        "authenticated": True,
                        "name": username,
                        "groups": [str(group) for group in groups]
                    }
                else:
                    return {
                        "authenticated": True,
                        "name": username,
                        "groups": [],
                    }
                return 
            else:
                return False
        except Exception as e:
            print(f"Erro ao autenticar: {e}")
            return False
        
    def is_admin(self, username, password):