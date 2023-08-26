var collapseAllButton = document.getElementById('collapse-all');
var expandAllButton = document.getElementById('expand-all');
var accordionItems = document.querySelectorAll('.accordion-item');
collapseAllButton.style.display = 'none';
expandAllButton.style.display = 'block';
collapseAllButton === null || collapseAllButton === void 0 ? void 0 : collapseAllButton.addEventListener('click', function () {
    accordionItems.forEach(function (item) {
        var collapseTarget = item.querySelector('.accordion-collapse');
        collapseTarget === null || collapseTarget === void 0 ? void 0 : collapseTarget.classList.remove('show');
        var button = item.querySelector('.accordion-button');
        button === null || button === void 0 ? void 0 : button.setAttribute('aria-expanded', 'false');
        button === null || button === void 0 ? void 0 : button.classList.add('collapsed');
    });
    collapseAllButton.style.display = 'none';
    expandAllButton.style.display = 'block';
});
expandAllButton === null || expandAllButton === void 0 ? void 0 : expandAllButton.addEventListener('click', function () {
    accordionItems.forEach(function (item) {
        var collapseTarget = item.querySelector('.accordion-collapse');
        collapseTarget === null || collapseTarget === void 0 ? void 0 : collapseTarget.classList.add('show');
        var button = item.querySelector('.accordion-button');
        button === null || button === void 0 ? void 0 : button.setAttribute('aria-expanded', 'true');
        button === null || button === void 0 ? void 0 : button.classList.remove('collapsed');
    });
    collapseAllButton.style.display = 'block';
    expandAllButton.style.display = 'none';
});
