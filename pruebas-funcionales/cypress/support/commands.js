Cypress.Commands.add('login', () => {

    cy.visit('/web/login');

    cy.get('#login')
        .should('be.visible')
        .type(Cypress.env('username'));

    cy.get('#password')
        .should('be.visible')
        .type(Cypress.env('password'));

    cy.get('button[type="submit"]')
        .click();

    // Esperar que Odoo cargue completamente
    cy.url({ timeout: 20000 })
        .should('include', '/odoo');

    // Esperar un momento para que aparezcan posibles notificaciones
    cy.wait(1000);

    cy.closeNotification();

});

Cypress.Commands.add('waitForOdoo', () => {

    // Esperar a que desaparezcan indicadores de carga
    cy.get('body').should('be.visible');

    cy.get('.o_loading_indicator', {
        timeout: 20000
    }).should('not.exist');

});


Cypress.Commands.add('closeNotification', () => {

    cy.document().then((doc) => {

        // Eliminar el contenedor de notificaciones
        doc.querySelectorAll('.o_notification_manager').forEach(el => el.remove());

        // Eliminar cada notificación individual
        doc.querySelectorAll('.o_notification').forEach(el => el.remove());

        // Eliminar el popup que muestra el mensaje
        doc.querySelectorAll('.text-break').forEach(el => {
            if (el.innerText.includes('Failed to enable push')) {
                el.closest('.o_notification')?.remove();
                el.remove();
            }
        });

    });

});


Cypress.Commands.add('goToInvoices', () => {

    cy.visit('/odoo/customer-invoices');

    cy.waitForOdoo();

    cy.closeNotification();

    cy.url().should('include', '/customer-invoices');

    cy.get('tbody tr', {
        timeout: 20000
    }).should('exist');

});

Cypress.Commands.add('openSearchPanel', () => {

    cy.closeNotification();

    cy.get('button[title="Toggle Search Panel"]', { timeout: 10000 })
        .should('be.visible')
        .click();

    cy.get('.o-dropdown--menu', { timeout: 10000 })
        .should('be.visible');

});