# ============================================================
# Pico Logic Analyzer Test
# Auteur : Potate_Bulle
# Projet : Raspberry Pi Pico W + Freenove Breakout Board + Logic Analyzer
#
# Description :
# Ce script sert à vérifier proprement les connexions entre une
# Raspberry Pi Pico / Pico WH(modèle) et un analyseur logique 24 MHz / 8 canaux.
#
# Chaque GPIO est activé l'un après l'autre avec une série d'impulsions.
# Dans PulseView, cela permet de confirmer que chaque canal D0 à D7
# reçoit bien le signal attendu.
#
# Matériel utilisé :
# - Raspberry Pi Pico WH
# - Freenove Breakout Board for Raspberry Pi Pico 1 / 2 / W / H / WH
# - Logic analyzer 24 MHz / 8 CH
# - Câbles Dupont
# - PulseView / Sigrok
# ============================================================

from machine import Pin
import time

# Mapping utilisé pour le test.
# Attention : dans PulseView, les canaux apparaissent souvent en D0 à D7.
# Sur mon analyseur logique, cela correspond à CH1 à CH8.
PINS = [
    ("CH1", "D0", "GP4", 4, "I2C SDA"),
    ("CH2", "D1", "GP5", 5, "I2C SCL"),
    ("CH3", "D2", "GP0", 0, "UART0 TX"),
    ("CH4", "D3", "GP1", 1, "UART0 RX / test signal"),
    ("CH5", "D4", "GP16", 16, "SPI0 RX / MISO / test signal"),
    ("CH6", "D5", "GP17", 17, "SPI0 CSn"),
    ("CH7", "D6", "GP18", 18, "SPI0 SCK / Clock"),
    ("CH8", "D7", "GP19", 19, "SPI0 TX / MOSI"),
]

outputs = []

for channel, pulseview_channel, gpio_name, gpio_num, role in PINS:
    pin = Pin(gpio_num, Pin.OUT)
    pin.value(0)
    outputs.append((channel, pulseview_channel, gpio_name, pin, role))


def reset_all():
    """Remet toutes les broches de test à l'état bas."""
    for channel, pulseview_channel, gpio_name, pin, role in outputs:
        pin.value(0)


def pulse_pin(channel, pulseview_channel, gpio_name, pin, role, pulses=20, delay=0.05):
    """
    Envoie une série d'impulsions sur une seule broche.

    Le but est volontairement simple : chaque canal doit bouger seul
    dans PulseView, ce qui rend le contrôle du câblage plus lisible.
    """
    print(f"Test {channel} / {pulseview_channel} -> {gpio_name} - {role}")

    reset_all()
    time.sleep(0.3)

    for _ in range(pulses):
        pin.value(1)
        time.sleep(delay)
        pin.value(0)
        time.sleep(delay)

    time.sleep(0.5)


def all_channels_wave():
    """
    Lance un motif simple sur tous les canaux.

    Cette étape permet de vérifier rapidement que tous les fils sont bien
    vus par l'analyseur logique après le test individuel.
    """
    print("Test final : motif alterné sur tous les canaux")

    reset_all()
    time.sleep(0.5)

    for _ in range(20):
        # Motif 10101010
        for index, (channel, pulseview_channel, gpio_name, pin, role) in enumerate(outputs):
            pin.value(index % 2)
        time.sleep(0.1)

        # Motif inversé 01010101
        for index, (channel, pulseview_channel, gpio_name, pin, role) in enumerate(outputs):
            pin.value((index + 1) % 2)
        time.sleep(0.1)

    reset_all()


print("========================================")
print("Pico Logic Analyzer Test")
print("Auteur : Potate_Bulle")
print("========================================")
print("Branchement attendu :")
print("CND/GND analyzer -> GND Pico")
print("CLK analyzer     -> non branche / isole")
print("CH1 a CH8        -> GPIO de test")
print("========================================")
print("Demarrage dans 2 secondes...")

time.sleep(2)

while True:
    print("\nDebut du cycle de test")

    for channel, pulseview_channel, gpio_name, pin, role in outputs:
        pulse_pin(channel, pulseview_channel, gpio_name, pin, role)

    all_channels_wave()

    print("Cycle termine. Pause 3 secondes.")
    time.sleep(3)
