/*
 * tems-examples-node
 * Copyright (c) 2017 Mentor Graphics (Quantix division)
 * LGPL-3.0
 */

import express from 'express';
import bodyParser from 'body-parser';
import bunyan from 'bunyan';
import routes from './routes';

const MAX_SIZE = '50mb';
const SERVICE_NAME = 'tems-catcher';
const app = express();


// Initialize our global logger
const logger = bunyan.createLogger({name: 'tems-examples-node'});
logger.level(bunyan.DEBUG);


// Increase the buffer sizes to handle large JSON payloads from the Tester
app.use(bodyParser.urlencoded({ extended: false, limit: MAX_SIZE }));
app.use(bodyParser.json({ limit: MAX_SIZE }));

// Install an error logger to catch any errors and log them and return 500
app.use((err, req, res, next) => {
    logger.error(err);
    res.status(500).send('Server error');
});

app.use('/', routes);

/* Ok -- all the setup is done .. launch the server and listen */
const port = process.env.TEMS_CATCHER_PORT || 3100;
app.set('port', port);
app.listen(port, () =>
    logger.info(`${SERVICE_NAME} is listening on port ${port}`)
);

export { logger };
