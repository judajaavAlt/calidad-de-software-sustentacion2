describe("Inicio de sesión", () => {

  it("Debe iniciar sesión correctamente", () => {

    cy.login("asprilla.andres@correounivalle.edu.co", "odooUVcalidad");

    cy.url().should("include", "/odoo/apps");
    

  });

});