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
                body: JSON.stringify({ name: battleName, data: formData })
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
        fetch(`/load_battle?name=${battleName}`)
            .then(response => response.json())
            .then(data => {
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

    function swapValues() {
        units.forEach(unit => {
            const attackInput = document.getElementById('attack_' + unit.toLowerCase());
            const defenseInput = document.getElementById('defense_' + unit.toLowerCase());
            const tempValue = attackInput.value;
            attackInput.value = defenseInput.value;
            defenseInput.value = tempValue;
        });
    }

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

    document.getElementById("clear-form-btn").addEventListener("click", clearForm);
    document.getElementById("save-battle-btn").addEventListener("click", saveBattle);
    document.getElementById("swap-values-btn").addEventListener("click", swapValues);
    document.getElementById("battle-type").addEventListener("change", updateVisibleUnits);

    var savedBattles = JSON.parse(localStorage.getItem('savedBattles')) || {};
    var savedBattlesList = document.getElementById('saved-battles-list');
    if (savedBattlesList) {
        for (var battleName in savedBattles) {
            if (savedBattles.hasOwnProperty(battleName)) {
                var listItem = document.createElement('li');
                listItem.className = 'list-group-item d-flex justify-content-between align-items-center';
                listItem.textContent = battleName;
                var buttonGroup = document.createElement('div');
                buttonGroup.className = 'button-group';
                var loadButton = document.createElement('button');
                loadButton.textContent = 'Load';
                loadButton.className = 'btn btn-sm btn-primary load-battle-btn';
                loadButton.dataset.battleName = battleName;
                var deleteButton = document.createElement('button');
                deleteButton.textContent = 'Delete';
                deleteButton.className = 'btn btn-sm btn-danger delete-battle-btn';
                deleteButton.dataset.battleName = battleName;
                buttonGroup.appendChild(loadButton);
                buttonGroup.appendChild(deleteButton);
                listItem.appendChild(buttonGroup);
                savedBattlesList.appendChild(listItem);
            }
        }
    }

    document.querySelectorAll(".load-battle-btn").forEach(button => {
        button.addEventListener("click", function(event) {
            event.preventDefault();
            loadBattle(button.dataset.battleName);
        });
    });

    document.querySelectorAll(".delete-battle-btn").forEach(button => {
        button.addEventListener("click", function(event) {
            event.preventDefault();
            deleteBattle(button.dataset.battleName);
        });
    });

    updateVisibleUnits();
});
