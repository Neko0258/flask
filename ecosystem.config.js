module.exports = {
  apps : [{
    name: 'Flask',
    script: '__init__.py',
    interpreter: '/usr/bin/python3',
    watch: true,
    env_development: {
      PORT: "3000",
      NODE_ENV: "development"
    },
    env_production: {
      PORT: "8080",
      NODE_ENV: "production"
    }
  }],

  deploy : {
    production : {
      user : 'neko',
      host : '172.16.2.97',
      ref  : 'origin/master',
      repo : 'git@github.com:Neko0258/flask.git',
      path : '/var/www/production',
      'pre-deploy-local': '',
      'post-deploy' : 'npm install && pm2 reload ecosystem.config.js --env production',
      'pre-setup': ''
    }
  }
};
