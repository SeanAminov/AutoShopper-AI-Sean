// Import with `import * as Sentry from "@sentry/node"` if you are using ESM



const Sentry = require("@sentry/node");

Sentry.init({
  dsn: "https://f9c642c0fbed9851a68015038374a11d@o4510370374615040.ingest.us.sentry.io/4510370599862272",
  // Setting this option to true will send default PII data to Sentry.
  // For example, automatic IP address collection on events
  sendDefaultPii: true,
});