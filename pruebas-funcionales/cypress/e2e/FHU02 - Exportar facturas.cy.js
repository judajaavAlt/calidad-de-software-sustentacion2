describe('FHU02 - Export invoices', () => {

    beforeEach(() => {
        cy.login();
        cy.closeNotification();
        cy.goToInvoices();
        cy.closeNotification();
    });

    it('Should display the export option', () => {

        cy.get('tbody tr')
            .first()
            .find('input[type="checkbox"]')
            .check({ force: true });

        cy.closeNotification();

        cy.contains('Actions').click();

        cy.contains('Export')
            .should('be.visible');

    });

});