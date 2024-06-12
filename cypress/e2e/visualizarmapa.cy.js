Cypress.Commands.add('deleteAllUsers', () => {
    cy.exec('python delete.py', { failOnNonZeroExit: true })
});

describe('teste visualizarmapa', () => {
    it('cenario1', () => {
        cy.visit('/');
        cy.exec('python manage.py migrate')
        cy.deleteAllUsers();

        cy.get(':nth-child(8)').click()
        cy.get('#inputFullName').type('Café Total')
        cy.get('#age4').type('25')
        cy.get('#inputgender4').select('Masculino')
        cy.get('.col-md-12 > .btn').click()
        cy.get('#inputEmail4').type('Ct@gmail.com')
        cy.get('#inputPassword4').type('12345')
        cy.get(':nth-child(4) > #inputPassword4').type('12345')
        cy.get('#gridCheck').click()
        cy.get('[type="submit"]').click()
        cy.get('#inputEmail4').type('Ct@gmail.com')
        cy.get('#inputPassword4').type('12345')
        cy.get('#inputStoreName').type('Café Total')
        cy.get('#inputAddress').type('Av. Cais do Apolo')
        cy.get('#inputAddress2').type('77')
        cy.get('#inputNeighborhood').type('Recife Antigo')
        cy.get('#inputZip').type('50030220')
        cy.get('#gridCheck').click()
        cy.get('.btn').click()
        cy.get('form > :nth-child(6)').click()
        cy.get('#inputFullName').type('Tonho')
        cy.get('#age4').type('28')
        cy.get('#inputgender4').select('Masculino')
        cy.get('.col-md-12 > .btn').click()
        cy.get('#inputEmail4').type('Tonho@gmail.com')
        cy.get('#inputPassword4').type('12345')
        cy.get(':nth-child(4) > #inputPassword4').type('12345')
        cy.get('#gridCheck').click()
        cy.get('[type="submit"]').click()
        cy.get('#inputEmail4').type('Tonho')
        cy.get('#inputPassword4').type('12345')
        cy.get('[type="submit"]').click()
    })
})
