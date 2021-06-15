/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5150', // the running FLASK api server url
  auth0: {
    url: 'blackmer.us', // the auth0 domain prefix
    audience: 'http://localhost:5150', // the audience set for the auth0 app
    clientId: '3azGCA3ahBiZYozjqfClcvwE6tDO8EhW', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:5150'
  }
};
