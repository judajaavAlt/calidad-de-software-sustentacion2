import './commands';

Cypress.on('uncaught:exception', (err) => {

    const ignoredErrors = [
        "Cannot read properties of null (reading 'parentNode')",
        "ResizeObserver loop limit exceeded",
        "Failed to enable push notifications"
    ];

    if (ignoredErrors.some(error => err.message.includes(error))) {
        return false;
    }

});