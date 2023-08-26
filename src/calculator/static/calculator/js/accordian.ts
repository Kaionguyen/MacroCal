const collapseAllButton = document.getElementById('collapse-all') as HTMLButtonElement;
const expandAllButton = document.getElementById('expand-all') as HTMLButtonElement;
const accordionItems = document.querySelectorAll('.accordion-item');

collapseAllButton.style.display = 'none';
expandAllButton.style.display = 'block';

collapseAllButton?.addEventListener('click', () => {
    accordionItems.forEach(item => {
        const collapseTarget = item.querySelector('.accordion-collapse');
        collapseTarget?.classList.remove('show');

        const button = item.querySelector('.accordion-button');
        button?.setAttribute('aria-expanded', 'false');
        button?.classList.add('collapsed');
    });

    collapseAllButton.style.display = 'none';
    expandAllButton.style.display = 'block';
});

expandAllButton?.addEventListener('click', () => {
    accordionItems.forEach(item => {
        const collapseTarget = item.querySelector('.accordion-collapse');
        collapseTarget?.classList.add('show');

        const button = item.querySelector('.accordion-button');
        button?.setAttribute('aria-expanded', 'true');
        button?.classList.remove('collapsed');
    });

    collapseAllButton.style.display = 'block';
    expandAllButton.style.display = 'none';
});

