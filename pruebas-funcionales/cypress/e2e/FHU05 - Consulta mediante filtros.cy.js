describe('FHU05 - Filter invoices', () => {

    beforeEach(() => {
        cy.login();
        cy.goToInvoices();
    });

    it('Should filter invoices', () => {

        cy.openSearchPanel();

        cy.contains('Filters')
            .click();

        cy.contains('Posted')
            .click();

    });

});