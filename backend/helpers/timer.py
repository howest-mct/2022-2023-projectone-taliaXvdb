import time

start_time = time.time()
elapsed_time = 0

while elapsed_time < 60:
    current_time = time.time()
    elapsed_time = current_time - start_time

    # Optioneel: Bereken resterende tijd en print het
    remaining_time = 60 - elapsed_time
    print("Resterende tijd:", remaining_time, "seconden")

    # Wacht een korte periode voordat de volgende meting wordt gedaan
    time.sleep(1)  # Wacht 1 seconde

print("Timer afgelopen!")