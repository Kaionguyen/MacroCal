const collapseAllButton = document.getElementById('collapse-all') as HTMLButtonElement;
const expandAllButton = document.getElementById('expand-all') as HTMLButtonElement;
const accordionItems = document.querySelectorAll('.accordion-item');

collapseAllButton.style.display = 'none';
expandAllButton.style.display = 'block';

collapseAllButton?.addEventListener('click', () => {
    accordionItems.forEach(item => {
        const collapseTarget = item.querySelector('.accordion-collapse');
        collapseTarget?.classList.remove('show');
    });

    collapseAllButton.style.display = 'none';
    expandAllButton.style.display = 'block';
});

expandAllButton?.addEventListener('click', () => {
    accordionItems.forEach(item => {
        const collapseTarget = item.querySelector('.accordion-collapse');
        collapseTarget?.classList.add('show');
    });

    collapseAllButton.style.display = 'block';
    expandAllButton.style.display = 'none';
});

