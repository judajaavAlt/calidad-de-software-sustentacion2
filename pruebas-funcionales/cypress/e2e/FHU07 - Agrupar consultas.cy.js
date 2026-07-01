describe('FHU07 - Group invoices', () => {

    beforeEach(() => {
        cy.login();
        cy.goToInvoices();
    });

    it('Should group invoices', () => {

        cy.openSearchPanel();

        cy.contains('Group By')
            .click();

        cy.contains('Customer')
            .click();

    });

});