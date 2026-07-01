describe("Verificación del entorno", () => {

  it("Debe abrir la página principal de Odoo", () => {
    cy.visit("/");
    cy.title().should("contain", "Odoo");
  });

});