describe('FHU01 - View invoices', () => {

    beforeEach(() => {
        cy.login();
        cy.goToInvoices();
    });

    it('Should display the invoice list', () => {

        cy.get('tbody tr')
            .should('have.length.greaterThan', 0);

    });

});