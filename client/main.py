#!/usr/bin/python3

# Nome: Cliente no terminal via REST API do Rock Album Vol 1
# Autor: Mateus Pinto da Silva
# Data: 25/09/2021

import routes


def router(EMAIL, IS_ADMIN):
    ADMIN = [
        ('[Administrador] Criar novo cartão presente', routes.admin__create_giftcard),
        ('[Administrador] Criar nova figurinha', routes.admin__create_stickers),
        ('[Administrador] Sortear prêmio da sorte', routes.admin__draw_lucky_prize),
        ('[Administrador] Tornar um jogador um administrador', routes.admin__op),
        ('[Administrador] Remover um jogador de administrador', routes.admin__unop),
    ]

    NON_ADMIN = [
        ('[Álbum] Ver seu próprio álbum', routes.album__get_album),
        ('[Álbum] Ver suas figurinhas livres (que não estão coladas nem a venda)', routes.album__get_free_stickers),
        ('[Álbum] Colar uma figurinha', routes.album__paste_sticker),
        ('[Mercado da comunidade] Comprar uma figurinha', routes.community_market__buy_sticker),
        ('[Mercado da comunidade] Ver preço de uma figurinha', routes.community_market__get_sticker_price),
        ('[Mercado da comunidade] Ver suas figurinhas à venda', routes.community_market__get_stickers_waiting_for_sale),
        ('[Mercado da comunidade] Colocar uma figurinha à venda', routes.community_market__put_sticker_to_sell),
        ('[Usuário] Ver suas moedas', routes.user__get_coins),
        ('[Usuário] Resgatar cartão-presente', routes.user__retrieve_giftcard),
        ('[Mercado oficial] Comprar pacote de figurinhas', routes.official_market__buy_sticker_pack),
        ('Sair', lambda *_: quit())
    ]

    ROUTES = ADMIN + NON_ADMIN if IS_ADMIN else NON_ADMIN

    while True:

        print('---- Menuzinho ----')
        for number, (description, _) in enumerate(ROUTES):
            print(f'{number} - {description};')
        print()

        option = int(input('Digite uma opção válida: '))
        try:
            F = ROUTES[option][1]
        except (IndexError, ValueError):
            F = lambda *_: print('Opção inválida!\n')

        F(EMAIL)
        input('Aperte enter para continuar...')


if __name__ == "__main__":
    EMAIL = routes.register() if input("Você deseja criar cadastro? [N/s] ").lower() == 's' else routes.login()
    IS_ADMIN = routes.is_admin(EMAIL)
    print()
    router(EMAIL, IS_ADMIN)
