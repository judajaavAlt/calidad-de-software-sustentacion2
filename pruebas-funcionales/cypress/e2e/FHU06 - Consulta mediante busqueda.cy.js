describe('FHU06 - Search invoices', () => {

    beforeEach(() => {
        cy.login();
        cy.goToInvoices();
    });

    it('Should search invoices by number', () => {

        cy.get('input[placeholder*="Search"]')
            .type('INV/2026/00008{enter}');

        cy.contains('INV/2026/00008')
            .should('exist');

    });

});