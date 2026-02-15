module.exports = {
  apps: [{
    name: 'codedungeon',
    cwd: '/home/dario/codeacademy/apps/web',
    script: 'node_modules/.bin/next',
    args: 'dev -p 3000',
    interpreter: 'node',
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    cron_restart: '0 */6 * * *',
    env: {
      NODE_ENV: 'development',
      PORT: '3000'
    },
    error_file: '/home/dario/.pm2/logs/codedungeon-error.log',
    out_file: '/home/dario/.pm2/logs/codedungeon-out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    merge_logs: true,
    restart_delay: 5000,
    max_restarts: 50,
    min_uptime: '30s'
  },
  {
    name: 'codedungeon-testing',
    cwd: '/home/dario/codeacademy-testing/apps/web',
    script: 'node_modules/.bin/next',
    args: 'dev -p 3001',
    interpreter: 'node',
    autorestart: true,
    watch: false,
    max_memory_restart: '1G',
    cron_restart: '0 */6 * * *',
    env: {
      NODE_ENV: 'development',
      PORT: '3001'
    },
    error_file: '/home/dario/.pm2/logs/codedungeon-testing-error.log',
    out_file: '/home/dario/.pm2/logs/codedungeon-testing-out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    merge_logs: true,
    restart_delay: 5000,
    max_restarts: 50,
    min_uptime: '30s'
  }]
};
