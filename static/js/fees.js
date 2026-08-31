// Fee Payment Modal & Calculation Engine
document.addEventListener('DOMContentLoaded', () => {
    const amountInput = document.getElementById('payment-amount-input');
    const netAmountSpan = document.getElementById('net-amount-span');
    const discountInput = document.getElementById('discount-amount-input');

    if (amountInput && discountInput && netAmountSpan) {
        function updateNet() {
            const total = floatVal(amountInput.value);
            const discount = floatVal(discountInput.value);
            const net = Math.max(0, total - discount);
            netAmountSpan.textContent = '$' + net.toFixed(2);
        }

        amountInput.addEventListener('input', updateNet);
        discountInput.addEventListener('input', updateNet);
    }

    function floatVal(val) {
        const parsed = parseFloat(val);
        return isNaN(parsed) ? 0.0 : parsed;
    }
});
