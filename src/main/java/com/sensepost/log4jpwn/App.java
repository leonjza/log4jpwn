package com.sensepost.log4jpwn;

import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.LogManager;

import static spark.Spark.*;

public class App
{
//    private static final Logger logger = LogManager.getLogger(App.class);
    static final Logger logger = LogManager.getLogger(App.class.getName());

    public static void main( String[] args )
    {

        port(8080);

        get("/", (req, res) -> {
            String ua = req.headers("User-Agent");
            System.out.println("Incoming User-Agent: " + ua);

            // trigger
            logger.error(ua);

            return "Logged User-Agent: " + ua;
        });
    }
}
