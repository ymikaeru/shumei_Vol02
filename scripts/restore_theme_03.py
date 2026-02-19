import json
import os

filepath = "Data/translated_parts/theme_03_霊主体従_part_02.json"

# The specific content for title_idx 2. This is constructed manually to be valid.
# Based on Step 256.
content_str = r'**Palestra de Meishu-Sama: "A Trindade dos Órgãos Internos"** (Julho de 1936)\n\n"De seguida, examinando a relação entre o Estômago, o Pulmão e o Coração...\n\nEm todas as artes médicas até hoje, devido à relação correspondente a \'Lua e Terra\', pesquisou-se bastante sobre \'Estômago e Pulmão\', mas parece que o \'Coração\' não foi muito aprofundado.\n\nSegundo a interpretação até hoje... considera-se que o sangue é purificado pelo movimento respiratório dos pulmões e retorna ao coração, mas,\n\nsegundo a nossa interpretação...,\n\na purificação do sangue é um \'trabalho conjunto do Pulmão e do Coração\'.\n\nA razão para isso é que o coração queima as \'impurezas no sangue\' com o \'Elemento Espiritual do Fogo\',\n\ne o pulmão lava o resíduo disso, que se poderia chamar de cinza...\n\nO sangue é purificado através disto, mas\n\na acumulação da última poluição gerada por essa \'purificação de Fogo e Água\'... torna-se também o maior fator como causa de doença.\n\nComparando isto, tem o mesmo significado que a poluição no chão ser desinfetada pela luz solar e lavada e purificada pela água da chuva.\n\nAqui, é necessário explicar a natureza do Fogo e da Água.\n\nOriginalmente, \'o Fogo arde através da Água, e a Água move-se através do Fogo\'.\n\nEm suma, o fogo tem tempo de arder porque existe humidade; se não houvesse humidade nenhuma, explodiria num instante.\n\nAlém disso, se a água não tivesse o calor do fogo, seria gelo e seria totalmente impossível fluir.\n\nÀ medida que se aquece a água com fogo, ela aquece e ferve... e gera-se força motriz.\n\nTambém a gasolina é água, e tanto o carvão mineral como o vegetal geram força de fogo ao arder continuamente porque contêm humidade.\n\nDo mesmo modo, a pressão da água na eletricidade hídrica flui devido ao calor, e o facto de as plantas crescerem e prosperarem deve-se à geração de força vital através do \'Fogo e Água\'.\n\nPela razão acima, a \'relação entre Coração e Pulmão\' é de Fogo e Água, portanto... se a força do fogo no coração for forte, a atividade do pulmão, que é água, torna-se vigorosa,\n\ne se houver muita humidade no pulmão, a atividade do coração, que é fogo, torna-se forte.\n\nO coração absorve continuamente o Elemento Espiritual (Elemento Fogo, que é calor solar) do \'Mundo dos Espíritos\' através da \'palpitação\',\n\ne o pulmão absorve continuamente o Elemento Ar (Elemento Hidrogénio, que é frio lunar) do \'Mundo Atmosférico\' através da \'respiração\',\n\ne o estômago é abastecido com \'alimentos\' (Elemento Terra, que é matéria) do \'Mundo Material\'.\n\nNós chamamos a isto a trindade dos órgãos internos.\n\nPelo facto de o coração absorver vigorosamente o Elemento Fogo, a emoção do amor torna-se vigorosa,\n\ne devido à força desse amor, desaparecem as raízes do conflito como o ódio, a inveja e o rancor, nascendo assim a paz.\n\n\nNo entanto, até hoje, devido à influência da cultura racionalista vinda de fora, absorvia-se mais o \'Elemento Frio da Lua\', oposto ao Elemento Fogo,\n\npor isso a emoção do amor tornou-se inevitavelmente escassa, e penso que isso se tornou a causa de disputas, guerras, doenças, etc.\n\nAlém disso, como a ciência é constituída por teorias académicas, inclina-se inevitavelmente para a razão,\n\ne isso também é uma causa poderosa... para tornar escassa a emoção do amor,\n\ne como resultado, tende-se inevitavelmente para o individualismo, tornando a sociedade humana realmente fria.\n\nDe facto, a razão pela qual há muitas pessoas com forte amor-próprio (egoísmo) entre os doentes pulmonares deve-se a este princípio.\n\nRecentemente, devido à influência da cultura estrangeira, etc., é natural que o número de pessoas com pulmões fracos tenha aumentado devido à falta de Elemento Espiritual do Fogo, ou seja, Espírito Japonês.\n\nPenso que o facto de até hoje não se ter compreendido a \'função do coração\' se deve ao facto de o Espírito Japonês estar adormecido.\n\nPela minha experiência a tratar muitos doentes pulmonares, há muitos adoradores da ciência, ou seja, do pensamento ocidental.\n\nO facto de haver muitos doentes pulmonares entre os comunistas, que se poderiam chamar de anti-Espírito Japonês, penso que conta vividamente esta história.\n\n\nPor razões como as acima, é essencial absorver, de qualquer forma, muito Elemento Espiritual do Fogo.\n\nComo resultado, o coração torna-se ativo, o pulmão torna-se saudável e a atividade do estômago também se torna vigorosa.\n\nPor isso, sabe-se que, como base da saúde, o mais importante é ser detentor do Espírito Japonês.\n\nFalando em termos latos, o desenvolvimento e expansão da cultura japonesa... que é o país que corresponde ao coração do mundo, fará despertar o \'Ocidente, que corresponde ao pulmão\',\n\ne o resultado será promover a felicidade e o desenvolvimento dos \'países não-culturais, que correspondem ao estômago\'.\n\nO que é a luz, afinal? É a \'união íntima de Fogo e Água\'...\n\nMesmo no ar, a luz é gerada pela \'união íntima de eletrões negativos e eletrões positivos\'... é a mesma razão.\n\nPor que razão a luz do Sol e a luz da Lua são diferentes...?\n\n [Image of Fire Water Diagram]\n\nComo acima,\n\nNa luz solar, o Fogo é principal e está na superfície, e a Água é secundária e Yin, ou seja, está no verso (fundo).\n\nNa luz lunar, a Água é principal e forma a superfície, e o Fogo é secundário e Yin, ou seja, está no verso.\n\nA Lua é um bloco frio como gelo, e brilha refletindo a \'Luz do Sol\' por trás,\n\ne o Sol é um \'bloco de Fogo\' que está sempre a arder, e brilha refletindo a \'Água da Lua\' por trás.\n\nPor isso, ambos são opostos; um é Yang e o outro é Yin, ou seja, gera-se a distinção entre \'Dia e Noite\'.\n\nO interessante é que o Fogo arde na vertical (Tate) e a Água flui na horizontal (Yoko). Possuem as propriedades de \'Vertical e Horizontal\'.\n\nA \'força vital\' nasce da união de coisas opostas como estas.\n\n [Image of Vertical Horizontal Diagram]\n\n Coração...   Fogo...   Vertical   |\n\n Pulmão...    Água...   Horizontal —\n\n Terra Estômago... Grande Terra... —\n\n\n\nO Fogo e a Água, se estiverem separados, não têm atividade nenhuma.\n\n\'Pela união de Fogo e Água, gera-se força motriz\'... como isso é a \'Grande Terra, ou seja, a terra do Estômago\', torna-se o carácter \'Terra\' (Tsuchi/Do), como mencionado anteriormente.\n\n\n\n           Vertical\n\n           Terra           Horizontal\n\n\n           Céu   Terra\n\n\nO significado da conclusão disto é \'Naru\' (Tornar-se/Completar), ou seja, \'Nari\' (Também/Ser), e torna-se \'Chi\' (Terra/Chão).\n\nNaru... Chi (Terra)\n\nOs casais humanos seguem a mesma lógica: o casal une-se, coopera, a atividade surge, geram filhos, gerem negócios e fazem a sociedade humana evoluir e desenvolver-se infinitamente." (Do "Registo das Palestras sobre a Arte de Curar do Professor Okada - Vol. 1 - 1")'

with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
skip = False

saw_title3 = False

for i, line in enumerate(lines):
    if skip:
        # Check for start of Item 3. "title_idx": 3 is unique for this file.
        # But we need to keep the preceding { and source_file.
        # It's safer to find the index of "title_idx": 3 FIRST.
        pass
    else:
        # Looking for the break point (after publication_title_ptbr of Item 2)
        if '"publication_title_ptbr": "A Trindade dos Órgãos Internos (Julho de 1936)"' in line:
            new_lines.append(line)
            # Add content line
            new_lines.append(f'    "content_ptbr": {json.dumps(content_str, ensure_ascii=False)}\n')
            # Add closing brace for Item 2
            new_lines.append('  },\n')
            skip = True
        else:
            new_lines.append(line)

# Now append Item 3 onwards
# Find line index where title_idx: 3 is.
idx3 = -1
for i, line in enumerate(lines):
    if '"title_idx": 3,' in line:
        idx3 = i
        break

if idx3 == -1:
    print("Could not find title_idx 3. Something wrong.")
    exit(1)

# Item 3 starts 2 lines before title_idx 3 strictly?
# Step 256: 
# 30:   },
# 31:   {
# 32:     "source_file": "sinra3.html",
# 33:     "title_idx": 3,
# So it starts at idx3 - 2.
rest_lines = lines[idx3 - 2:]
new_lines.extend(rest_lines)

with open(filepath, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

try:
    with open(filepath, "r", encoding="utf-8") as f:
        json.load(f)
    print("SUCCESS: JSON is valid.")
except Exception as e:
    print(f"ERROR: JSON is still invalid: {e}")

