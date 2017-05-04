/*
 * us-tems-catcher
 * Copyright (c) 2016 Mentor Graphics (Quantix division)
 * UNLICENSED
 */

import {Router as createRouter} from 'express';

import {logger} from '../server';
import {
    validateTestCell,
    extractIds,
    getMessage,
    getJobType,
    addToQ,
    finalize
} from './helper';

const router = createRouter();
const ROUTE_PREFIX = '/tems/TEST_CELL';

router.post(`${ROUTE_PREFIX}/:testCell/LOT/:lotId/SUBLOT/:sublotId/:eventId`,
    validateTestCell,
    extractIds,
    getMessage,
    getJobType,
    addToQ,
    finalize,
    (req, res) => {
        logger.debug('Saw SUBLOT_ Message! with body of ', req.body);
        res.status(200);
        res.json({
            success: true,
            message: `Sublot '${req.subLot}' has been processed`
        });
    }
);

router.post(`${ROUTE_PREFIX}/:testCell/LOT/:lotId/:eventId`,
    validateTestCell,
    extractIds,
    getMessage,
    getJobType,
    addToQ,
    finalize,
    (req, res) => {
        logger.debug('Saw LOT_ Message! with body of ', req.body);
        res.status(200);
        res.json({
            success: true,
            message: `Lot '${req.lotId}' has been processed`
        });
    }
);

router.post(`${ROUTE_PREFIX}/:testCell/:eventId`,
    validateTestCell,
    extractIds,
    getMessage,
    getJobType,
    addToQ,
    finalize,
    (req, res) => {
        logger.debug(`Saw ${req.eventId} Message! with body of `, req.body);
        res.status(200);
        res.json({
            success: true,
            message: `'${req.eventId}' event has been processed`
        });
    }
);

export default router;
