// Wait until the DOM is fully loaded before running the script
document.addEventListener("DOMContentLoaded", function() {

    // Function to clear the form inputs
    function clearForm() {
        var form = document.getElementById("battle-form");
        if (form) {
            var inputs = form.getElementsByTagName('input');
            for (var i = 0; i < inputs.length; i++) {
                if (inputs[i].type === 'number') {
                    inputs[i].value = 0;  // Reset number inputs to 0
                } else {
                    inputs[i].value = '';  // Reset other input types to empty strings
                }
            }
            // Clear the URL query string without reloading the page
            window.history.replaceState({}, document.title, window.location.pathname);
        }
    }

    // Function to save the current battle configuration
    function saveBattle() {
        var battleName = prompt("Enter a name for your saved battle:");
        if (battleName) {
            var formData = {};
            var inputs = document.getElementsByTagName('input');
            for (var i = 0; i < inputs.length; i++) {
                formData[inputs[i].name] = inputs[i].value;  // Collect input values into formData
            }
            var battleType = document.getElementById('battle-type').value;  // Get selected battle type
            var savedBattles = JSON.parse(localStorage.getItem('savedBattles')) || {};  // Load saved battles from local storage
            savedBattles[battleName] = { data: formData, type: battleType };  // Save the current battle under the given name
            localStorage.setItem('savedBattles', JSON.stringify(savedBattles));  // Save updated battles back to local storage
            location.reload();  // Reload the page to update the UI
        }
    }

    // Function to load a previously saved battle configuration
    function loadBattle(battleName) {
        var savedBattles = JSON.parse(localStorage.getItem('savedBattles')) || {};  // Load saved battles from local storage
        var battle = savedBattles[battleName] || {};  // Get the selected battle data
        var data = battle.data || {};  // Get the battle's form data
        for (var key in data) {
            if (data.hasOwnProperty(key)) {
                var input = document.getElementsByName(key)[0];
                if (input) {
                    input.value = data[key];  // Set form input values based on saved data
                }
            }
        }
        if (battle.type) {
            document.getElementById('battle-type').value = battle.type;  // Set the battle type dropdown
            updateVisibleUnits();  // Update the visible units based on the battle type
        }
    }

    // Function to delete a saved battle
    function deleteBattle(battleName) {
        if (confirm(`Are you sure you want to delete the battle "${battleName}"?`)) {
            var savedBattles = JSON.parse(localStorage.getItem('savedBattles')) || {};  // Load saved battles from local storage
            delete savedBattles[battleName];  // Remove the selected battle
            localStorage.setItem('savedBattles', JSON.stringify(savedBattles));  // Save the updated list back to local storage
            location.reload();  // Reload the page to update the UI
        }
    }

    // Function to swap attack and defense values for each unit
    function swapValues() {
        units.forEach(unit => {
            const attackInput = document.getElementById('attack_' + unit.toLowerCase());
            const defenseInput = document.getElementById('defense_' + unit.toLowerCase());
            const tempValue = attackInput.value;  // Temporarily store the attack value
            attackInput.value = defenseInput.value;  // Set attack value to defense value
            defenseInput.value = tempValue;  // Set defense value to the original attack value
        });
    }

    // Function to update the visible units based on the selected battle type
    function updateVisibleUnits() {
        const unitsByBattleType = {
            land: ['infantry', 'artillery', 'tank', 'fighter', 'bomber', 'aa'],
            amphibious: ['infantry', 'artillery', 'tank', 'fighter', 'bomber', 'cruiser', 'battleship', 'aa'],
            sea: ['fighter', 'bomber', 'submarine', 'destroyer', 'cruiser', 'carrier', 'battleship']
        };

        const battleType = document.getElementById('battle-type').value;
        const visibleUnits = unitsByBattleType[battleType];

        document.querySelectorAll('.unit-row').forEach(row => {
            const unit = row.getAttribute('data-unit');
            const attackInput = document.getElementById('attack_' + unit.toLowerCase());
            const defenseInput = document.getElementById('defense_' + unit.toLowerCase());
            if (visibleUnits.includes(unit)) {
                row.style.display = 'flex';  // Display the row if the unit is relevant for the battle type
            } else {
                row.style.display = 'none';  // Hide the row if the unit is not relevant
                attackInput.value = 0;  // Reset the attack value
                defenseInput.value = 0;  // Reset the defense value
            }
        });
    }

    // Function to display unit statistics in a modal
    function showUnits() {
        fetch('static/units.json')  // Fetch unit data from a JSON file
            .then(response => response.json())
            .then(units => {
                var modalContent = document.getElementById('units-modal-content');
                modalContent.innerHTML = '';  // Clear existing content

                // Populate modal with unit statistics
                for (var unit in units) {
                    if (units.hasOwnProperty(unit)) {
                        var unitData = units[unit];
                        var unitInfo = document.createElement('p');
                        unitInfo.textContent = `${unit}: Attack: ${unitData.attack}, Defense: ${unitData.defense}, IPC: ${unitData.ipc}`;
                        modalContent.appendChild(unitInfo);
                    }
                }

                // Display the modal using Bootstrap's modal component
                var modal = new bootstrap.Modal(document.getElementById('units-modal'));
                modal.show();
            })
            .catch(error => console.error('Error fetching units:', error));
    }

    // Function to quickly simulate a battle and display the results
    function quickSimulate() {
        const formData = new FormData(document.getElementById("battle-form"));
        fetch("/quick_simulate", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            document.getElementById("results-content-attacker").innerHTML = `<p>Attacker Wins: ${data.attacker_win_percentage}%</p>`;
            document.getElementById("results-content-defender").innerHTML = `<p>Defender Wins: ${data.defender_win_percentage}%</p>`;
            document.getElementById("results-content-ties").innerHTML = `<p>Ties: ${data.tie_percentage}%</p>`;
        })
        .catch(error => console.error("Error:", error));
    }

    // Event listeners for various buttons and dropdowns
    document.getElementById("clear-form-btn").addEventListener("click", clearForm);
    document.getElementById("save-battle-btn").addEventListener("click", saveBattle);
    document.getElementById("swap-values-btn").addEventListener("click", swapValues);
    document.getElementById("show-units-btn").addEventListener("click", showUnits);
    document.getElementById("quick-sim-btn").addEventListener("click", quickSimulate);
    document.getElementById("battle-type").addEventListener("change", updateVisibleUnits);

    // Load and display saved battles in the UI
    var savedBattles = JSON.parse(localStorage.getItem('savedBattles')) || {};
    var savedBattlesList = document.getElementById('saved-battles-list');
    if (savedBattlesList) {
        for (var battleName in savedBattles) {
            if (savedBattles.hasOwnProperty(battleName)) {
                var listItem = document.createElement('li');
                listItem.className = 'list-group-item d-flex justify-content-between align-items-center';
                listItem.textContent = battleName;

                // Create buttons for loading and deleting the saved battle
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

    // Event listeners for dynamically generated load and delete buttons
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

    // Initial call to update the visible units based on the current battle type
    updateVisibleUnits();
});
