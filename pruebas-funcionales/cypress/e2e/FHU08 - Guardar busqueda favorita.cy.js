describe('FHU08 - Save favorite search', () => {

    beforeEach(() => {
        cy.login();
        cy.goToInvoices();
    });

    it('Should save the current search as favorite', () => {

        // Abrir el panel de búsqueda
        cy.openSearchPanel();

        // Abrir Filters
        cy.contains('Filters')
            .should('be.visible')
            .click();

        // Aplicar el filtro Posted (igual que la FHU05)
        cy.get('.o-dropdown--menu')
            .within(() => {
                cy.contains('span.o-dropdown-item.o_menu_item', /^Posted$/)
                    .click();
            });

        // Esperar a que se aplique el filtro
        cy.wait(1000);

        // Guardar la búsqueda actual
        cy.get('button.o_add_favorite', { timeout: 10000 })
            .should('be.visible')
            .click();

        // Escribir el nombre del filtro
        cy.get('input.o_input.my-1', { timeout: 10000 })
            .should('be.visible')
            .clear()
            .type('Posted Invoices');

        // Guardar
        cy.get('button.o_save_favorite', { timeout: 10000 })
            .should('be.visible')
            .click();

    });

});