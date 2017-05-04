import fs from 'fs';
import path from 'path';
import moment from 'moment';
import {logger, createReplayFile, replayFileDir, addToQueue} from '../server';

const WANTED_MESSAGES = [
    'INITIALIZATION', 'STATUS', 'CONFIGURATION',
    'TESTER_OS', 'TEST_PROGRAM_LOAD', 'MAINTENANCE',
    'LOT_START', 'LOT_END', 'SUBLOT_START', 'SUBLOT_END',
    'TEST_START', 'TEST_DATA', 'TEST_END',
    'CZ_START', 'CZ_SETUP', 'CZ_START_POINT',
    'CZ_DATA_POINT', 'CZ_SUMMARY', 'CZ_END',
    'SHUTDOWN'
];

// GNG-1225: Fix TODO and finally add a set of replay files, one per tester.
const testerStreams = new Map();

export function validateTestCell(req, res, next) {
    if (!req.params.testCell) {
        const message = 'Test Cell ID is missing';
        logger.warn(message);

        res.status(400).send({
            message,
            success: false
        });
    } else {
        next();
    }
}

export function extractIds(req, res, next) {
    const {params: {testCell, lotId, sublotId, eventId}} = req;

    req.lot = lotId;
    req.subLot = sublotId;
    req.testCell = testCell;
    req.eventId = eventId;

    next();
}

export function getMessage(req, res, next) {
    const {eventId} = req;
    logger.trace(`Saw TEMS Message for ${eventId} event`);

    req.qEvent = eventId;

    switch (eventId) {
    case 'INITIALIZATION' :
        logger.trace(`Saw TEMS INIT Message for tester ${req.testerId} with body of ${req.body}`);

        /**
         * What messages do we want.. why, all of them!
         * Alas, there is no wildcard in the TEMS spec,
         * so we need to make sure we keep the list up to date..
         */
        Object.assign(req.body, WANTED_MESSAGES);
        break;

    case 'SHUTDOWN' : {
        logger.trace(`SHUTDOWN message seen for tester ${req.testerId} removing stream`);

        // If we have an open filestream then close it...
        const openStream = testerStreams.get(req.testerId);
        if (openStream) {
            logger.trace('Found open replay stream -- closing');
            openStream.end();
            testerStreams.delete(req.testerId);
        }
        break;
    }

    default :
    }

    next();
}

export function getJobType(req, res, next) {
    const {testCell, lot, subLot} = req;

    let jobType = 'Test Cell';

    if (subLot) {
        jobType = 'Sublot';
    } else if (lot) {
        jobType = 'Lot';
    }

    logger.trace(`Processing ${jobType} for ${testCell}`);

    next();
}

/* addToQ - Add the latest message to the job queue for the tems worker(s) to process.. */
export function addToQ(req, res, next) {
    const event = req.qEvent || 'UNKNOWN';
    const {url, body, params, testCell, lot, subLot} = req;

    // SJM - New option to NOT queue the message to be processed ..
    // Used only for severe debugging where you just want to capture the TEMS stream
    if (!addToQueue) {
        logger.debug(`DEBUG MODE - NOT QUEUEING MESSAGE! URI ${url}  with event of ${event}`);
        next();

        return;
    }

    // Ok -- normal processing commences..enqueue message
    logger.debug(`Adding URI ${url} to Job Q with event of ${event}`);
    logger.debug('CTX Params are: ', params);

    next();
}

async function saveTems(req, res, next) {
    const {url, body, testCell} = req;

    // See if we have a replatStream or not already..if not create one
    let replayStream = testerStreams.get(testCell);
    if (!replayStream) {
        // Format the curernt date/time into the style we like for replay files
        const dateFmt = moment().format('YYYYMMDDHHmmss');

        /* Create an instance of our dumper class for this tester ... */
        const streamName = path.join(replayFileDir, `${testCell}-${dateFmt}-replay.txt`);
        replayStream = fs.createWriteStream(streamName);
        testerStreams.set(testCell, replayStream);
    }

    if (replayStream) {
        replayStream.write(`${JSON.stringify({url, body})}\n`);
    }

    await next();
}

export const finalize = createReplayFile ? saveTems : (req, res, next) => {
    logger.trace('Not writing replay file');

    next();
};
