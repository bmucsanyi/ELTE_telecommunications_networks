Mondjuk egy áruházat kell megvalósítani
A szerver egy áruház
A kliens egy vásárló

A kliens megad a bemenetre egy árut és hogy hány darabot szeretne belőle
Ha azt küldi, hogy "END 0" akkor befejezi a vásárlást
És a szerver válaszul elküldi, hogy mennyit kell fizetnie azokért amik vannak raktáron.
És mik voltak amik nincsenek raktáron (egyetlen stringként, vesszővel felsorolva).

A raktár az mondjuk egy dict a szerverben, hogy mi az áru neve, és mennyibe kerül

Ha akarsz nehezítést
Akkor egy proxy van a közepén
És itt már ő tudja, hogy van e olyan áru
És csak az árat továbbítja a szervernek ami tényleg van
A szerver a végén összeadja és visszaküldi a kliensnek