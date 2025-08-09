# Cifras
2024-02-20
:sectlinks:
:icons: font
:jbake-type: page
:up: icon:long-arrow-alt-up[fw]
:dn: icon:long-arrow-alt-down[fw]
:b: [.big]
:s: [.small]
:table-caption: Exemplo


== Nomes do acordes/notas

[%header,format=csv]
|===
Dó, Ré, Mi, Fá, Sol, Lá, Si
C, D, E, F, G, A, B
|===

== Acidentes

[%header,format=csv]
|===
Bemol, Sustenido, Duplo bemol, Duplo sustenido
b ou &<mark>x266D;, # ou &#x266F;, bb ou &#x1d12b;, #</mark> ou &#x1d12a;
|===

== Outros Símbolos

Estes simbolos eu uso para aumentar a informação disponível na cifra para facilitar a execução da música:

[square]
* [repeticao-de-acorde](#repeticao-de-acorde)
* [pausa](#pausa)
* [divisao](#divisao)
* [subdivisao](#subdivisao)
* [grupos](#grupos)
* [mudanca-compasso](#mudanca-compasso)
* [anacruse](#anacruse)
* [marcar-tempo](#marcar-tempo)


<a name="repeticao-de-acorde"></a> % (repetição de acorde):: indica que o mesmo acorde deve ser tocado por mais 1 batida (ou compasso), e.g., *** C % ***.

.em compasso 3/4:
[.center,subs="attributes",cols="12*^.^"]
|===
| C   |     |     |     |     |     | %   |     |     |     |     |

|{dn} |{up} |{dn} |{up} |{dn} |{up} |{dn} |{up} |{dn} |{up} |{dn} |{up}
| **1** |^e^  |~2~  |^e^  |~3~  |^e^  | **1** |^e^  |~2~  |^e^  |~3~  |^e^
|===

<a name="pausa"></a> // (pausa):: indica uma pausa na batida, descontada do tempop da própria batida (ou compasso) devendo a batida ser retomada dentro do tempo normalmente no próximo acorde.

<a name="divisao"></a> * (divisão):: indica a divisão do tempo da batida (ou compasso) entre os acordes anterior e posterior à marca, e.g., *** C * D ***, onde a batida é dividida meio à meio entre os acordes ***C*** e ***D****. Pode ser usado para indicar divisão em 3 partes iguais, e.g., *** C * D * E **.

[.center,subs="attributes+",cols="8*^.^"]
|===
| C   |     | *   |     | D   |     |     |

|{dn} |{up} |{dn} |{up} |{dn} |{up} |{dn} |{up}
|**1**  |^e^  |~2~  |^e^  | 3   |^e^  |~4~  |^e^
|===

<a name="subdivisao"></a> *** (subdivisão):: indica a divisão do tempo já dividido da batida (ou compasso) entre os acordes, e.g., *** C * D +***+ E ***, onde ***C*** é tocado por meia batida (ou compasso) e ***D*** e ***E*** dividem igualmente a outra metade. Pode-se dividir a outra metade em 3 partes iguais também, e.g., *** C * D +****+ E +****+ F ***.

[.center,subs="attributes",cols="8*^.^"]
|===
| C   |     | *   |     | D   | **  | E   |

|{dn} |{up} |{dn} |{up} |{dn} |{up} |{dn} |{up}
|**1**  |^e^  |~2~  |^e^  | 3   |^e^  |~4~  |^e^
|===

<a name="grupos"></a> ( ) (grupos):: use *** ( ) *** para delimitar grupos se necessário, e.g., *** C * (D +****+ E) ***.


<a name="mudanca-compasso"></a> &M/N &M/N: (mudança de compasso):: #&***M/N****:# ou #&****M/N****# onde **M/N*** é o novo compasso. Caso tenha **:** a mudança afeta apenas o próximo compasso retornando ao compasso anterior logo após. Caso não tenha ***:***, a mudança segue até o fim ou até uma nova alteração.

<a name="anacruse"></a> ? (anacruse):: indicada por ***?*** no início ou no fim, e.g., *** ? C D *** ou *** C D ? ***. Anacruse é um compasso que não está completo, no início ou no fim da música. No caso do violão, indica que haverá algum instrumentos tocando uma melodia parcial antes da entrada ou depois da saída do instrumento, ou que a batida irá começar/terminar parcialmente.

<a name="marcar-tempo"></a> ! !. !! (marcar/reforçar tempo):: indicada por **!!** ao lado do acorde, e.g., **C!!**. Indica que a batida deve ser alterada para somente para baixo, preferencialmente no graves, marcando bem o tempo/ritmo da música. **!.** indica preferencialmente nos agudos. **!** indica alternância entre graves e agudas.

[.center,subs="attributes",cols="8*^.^"]
|===
| C!!  7+| (tocar somente para baixo)

|{dn} |{dn} |{dn} |{dn} |{dn} |{dn} |{dn} |{dn}
|**1**  |^e^  |~2~  |^e^  | 3   |^e^  |~4~  |^e^
|===
