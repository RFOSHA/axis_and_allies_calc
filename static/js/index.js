document.addEventListener('DOMContentLoaded', function() {
    const unitsByBattleType = {
        land: ['infantry', 'artillery', 'tank', 'fighter', 'bomber', 'aa'],
        amphibious: ['infantry', 'artillery', 'tank', 'fighter', 'bomber', 'cruiser', 'battleship', 'aa'],
        sea: ['fighter', 'bomber', 'submarine', 'destroyer', 'cruiser', 'aircraft carrier', 'battleship']
    };

    function updateVisibleUnits() {
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

    document.getElementById('battle-type').addEventListener('change', updateVisibleUnits);
    document.getElementById('swap-values-btn').addEventListener('click', function() {
        const unitNames = {{ units.keys()|list|tojson }};
        unitNames.forEach(unit => {
            const attackInput = document.getElementById('attack_' + unit.toLowerCase());
            const defenseInput = document.getElementById('defense_' + unit.toLowerCase());
            const tempValue = attackInput.value;
            attackInput.value = defenseInput.value;
            defenseInput.value = tempValue;
        });
    });

    updateVisibleUnits(); // Initial call to set the correct units on page load
});