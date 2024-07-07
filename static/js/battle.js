document.addEventListener("DOMContentLoaded", function() {
    function clearForm() {
        var form = document.getElementById("battle-form");
        if (form) {
            var inputs = form.getElementsByTagName('input');
            for (var i = 0; i < inputs.length; i++) {
                if (inputs[i].type === 'number') {
                    inputs[i].value = 0;
                } else {
                    inputs[i].value = '';
                }
            }
            window.history.replaceState({}, document.title, window.location.pathname);
        }
    }

    function saveBattle() {
        var battleName = prompt("Enter a name for your saved battle:");
        if (battleName) {
            var formData = {};
            var inputs = document.getElementsByTagName('input');
            for (var i = 0; i < inputs.length; i++) {
                formData[inputs[i].name] = inputs[i].value;
            }
            fetch('/save_battle', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({name: battleName, data: formData})
            }).then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    alert("Failed to save battle");
                }
            });
        }
    }

    function loadBattle(battleName) {
        fetch(`/load_battle?name=${battleName}`).then(response => response.json()).then(data => {
            for (var key in data) {
                if (data.hasOwnProperty(key)) {
                    var input = document.getElementsByName(key)[0];
                    if (input) {
                        input.value = data[key];
                    }
                }
            }
        });
    }

    function deleteBattle(battleName) {
        if (confirm(`Are you sure you want to delete the battle "${battleName}"?`)) {
            fetch(`/delete_battle?name=${battleName}`, {
                method: 'DELETE'
            }).then(response => {
                if (response.ok) {
                    location.reload();
                } else {
                    alert("Failed to delete battle");
                }
            });
        }
    }

    // Function to swap values between attacking and defending units
    function swapValues() {
        units.forEach(unit => {
            const attackInput = document.getElementById('attack_' + unit.toLowerCase());
            const defenseInput = document.getElementById('defense_' + unit.toLowerCase());
            const tempValue = attackInput.value;
            attackInput.value = defenseInput.value;
            defenseInput.value = tempValue;
        });
    }

    // Function to update visible units based on selected battle type
    function updateVisibleUnits() {
        const unitsByBattleType = {
            land: ['infantry', 'artillery', 'tank', 'fighter', 'bomber', 'aa'],
            amphibious: ['infantry', 'artillery', 'tank', 'fighter', 'bomber', 'cruiser', 'battleship', 'aa'],
            sea: ['fighter', 'bomber', 'submarine', 'destroyer', 'cruiser', 'aircraft carrier', 'battleship']
        };

        const battleType = document.getElementById('battle-type').value;
        const visibleUnits = unitsByBattleType[battleType];

        document.querySelectorAll('.unit-row').forEach(row => {
            const unit = row.getAttribute('data-unit');
            if (visibleUnits.includes(unit)) {
                row.style.display = 'flex';
            } else {
                row.style.display = 'none';
            }
        });
    }

    // Attach event listeners
    document.getElementById("clear-form-btn").addEventListener("click", clearForm);
    document.getElementById("save-battle-btn").addEventListener("click", saveBattle);
    document.getElementById("swap-values-btn").addEventListener("click", swapValues);
    document.getElementById("battle-type").addEventListener("change", updateVisibleUnits);

    document.querySelectorAll(".load-battle-btn").forEach(button => {
        button.addEventListener("click", function() {
            loadBattle(button.dataset.battleName);
        });
    });
    document.querySelectorAll(".delete-battle-btn").forEach(button => {
        button.addEventListener("click", function() {
            deleteBattle(button.dataset.battleName);
        });
    });

    updateVisibleUnits(); // Initial call to set the correct units on page load
});
