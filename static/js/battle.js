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
            var battleType = document.getElementById('battle-type').value;
            var savedBattles = JSON.parse(localStorage.getItem('savedBattles')) || {};
            savedBattles[battleName] = { data: formData, type: battleType };
            localStorage.setItem('savedBattles', JSON.stringify(savedBattles));
            location.reload();
        }
    }

    function loadBattle(battleName) {
        var savedBattles = JSON.parse(localStorage.getItem('savedBattles')) || {};
        var battle = savedBattles[battleName] || {};
        var data = battle.data || {};
        for (var key in data) {
            if (data.hasOwnProperty(key)) {
                var input = document.getElementsByName(key)[0];
                if (input) {
                    input.value = data[key];
                }
            }
        }
        if (battle.type) {
            document.getElementById('battle-type').value = battle.type;
            updateVisibleUnits();
        }
    }

    function deleteBattle(battleName) {
        if (confirm(`Are you sure you want to delete the battle "${battleName}"?`)) {
            var savedBattles = JSON.parse(localStorage.getItem('savedBattles')) || {};
            delete savedBattles[battleName];
            localStorage.setItem('savedBattles', JSON.stringify(savedBattles));
            location.reload();
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
            const attackInput = document.getElementById('attack_' + unit.toLowerCase());
            const defenseInput = document.getElementById('defense_' + unit.toLowerCase());
            if (visibleUnits.includes(unit)) {
                row.style.display = 'flex';
            } else {
                row.style.display = 'none';
                attackInput.value = 0;
                defenseInput.value = 0;
            }
        });
    }

    function showUnits() {
        fetch('static/units.json')
            .then(response => response.json())
            .then(units => {
                var modalContent = document.getElementById('units-modal-content');
                modalContent.innerHTML = '';

                for (var unit in units) {
                    if (units.hasOwnProperty(unit)) {
                        var unitData = units[unit];
                        var unitInfo = document.createElement('p');
                        unitInfo.textContent = `${unit}: Attack: ${unitData.attack}, Defense: ${unitData.defense}, IPC: ${unitData.ipc}`;
                        modalContent.appendChild(unitInfo);
                    }
                }

                var modal = new bootstrap.Modal(document.getElementById('units-modal'));
                modal.show();
            })
            .catch(error => console.error('Error fetching units:', error));
    }

    function quickSimulate() {
        const formData = new FormData(document.getElementById("battle-form"));
        fetch("/quick_simulate", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById("results-content-attacker").innerHTML = `<p>Attacker Wins: ${data.attacker_win_count}</p>`;
            document.getElementById("results-content-defender").innerHTML = `<p>Defender Wins: ${data.defender_win_count}</p>`;
            document.getElementById("results-content-ties").innerHTML = `<p>Ties: ${data.ties}</p>`;
        })
        .catch(error => console.error("Error:", error));
    }

    document.getElementById("clear-form-btn").addEventListener("click", clearForm);
    document.getElementById("save-battle-btn").addEventListener("click", saveBattle);
    document.getElementById("swap-values-btn").addEventListener("click", swapValues);
    document.getElementById("show-units-btn").addEventListener("click", showUnits);
    document.getElementById("quick-sim-btn").addEventListener("click", quickSimulate);
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
