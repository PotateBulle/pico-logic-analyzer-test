# Wiring Notes

Ce document résume le câblage utilisé pour relier un logic analyzer 24 MHz / 8 CH à une Raspberry Pi Pico WH montée sur une Freenove Breakout Board.

## Mapping final

```text
CND -> GND Pico
CLK -> non branché, isolé

CH1 -> GP4   -> I2C SDA
CH2 -> GP5   -> I2C SCL

CH3 -> GP0   -> UART0 TX
CH4 -> GP1   -> UART0 RX

CH5 -> GP16  -> SPI0 RX / MISO
CH6 -> GP17  -> SPI0 CSn
CH7 -> GP18  -> SPI0 SCK
CH8 -> GP19  -> SPI0 TX / MOSI
```

## Correspondance PulseView

PulseView affiche souvent les canaux sous la forme `D0` à `D7`.

```text
D0 = CH1
D1 = CH2
D2 = CH3
D3 = CH4
D4 = CH5
D5 = CH6
D6 = CH7
D7 = CH8
```

## Pourquoi brancher la masse ?

Le logic analyzer doit partager la même référence de masse que la Pico. Sans masse commune, les signaux peuvent être illisibles ou complètement faux.

```text
CND / GND analyzer -> GND Pico
```

## Pourquoi ne pas brancher CLK ?

Sur ce type d'analyseur logique, la broche `CLK` peut servir à des modes particuliers avec horloge externe. Pour une utilisation normale avec PulseView, elle n'est pas nécessaire.

Pour le SPI, le signal d'horloge est branché sur un canal classique :

```text
CH7 / D6 -> GP18 / SPI0 SCK
```

## Conseil pratique

Les couleurs des câbles ne sont pas une source fiable. Il faut suivre les étiquettes du connecteur : `CH1`, `CH2`, `CH3`, etc.

Les couleurs peuvent changer selon les fabricants, mais les labels restent la référence.
