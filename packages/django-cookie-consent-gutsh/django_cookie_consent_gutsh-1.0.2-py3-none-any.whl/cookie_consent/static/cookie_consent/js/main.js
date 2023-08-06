const LIBRARY = "Cookie consent"
const VERSION = "0.1.0"
const LOG_STR = LIBRARY + ' ' + VERSION
const LS_TOKEN = 'cookie_consent_status'

const acptBtn = document.querySelector('.cookie-consent > button'),
      closBtn = document.querySelector('.cookie-consent > header .close'),
      consentElem = closBtn?.parentNode?.parentNode

async function reportAcceptance() {
    const REQ_STR = "cookie consent acceptance:"

    let response

    return fetch('/cookie_consent/accept').then(
        res => {
            response = res
            return res.json()
        }
    ).catch(
        e => {
            console.warn(LOG_STR, REQ_STR, e)
            return response.text()
        }
    ).then(
        content => {
            console.log(LOG_STR, REQ_STR, content)
        }
    ).catch(
        (e) => console.error(LOG_STR, REQ_STR, e)
    )
}

function removeConsentElement(requester) {
    let consent
    switch (requester) {
        case acptBtn:
            consent = requester.parentNode
            break
        case closBtn:
            consent = requester.parentNode.parentNode
            break
        default:
            consent = consentElem
    }
    console.assert(Object.is(consent, consentElem), "shouldn't happen")
    console.debug(LOG_STR, 'found consent elem', consent)
    consent.remove()
}

async function acceptCoookies(e) {
    console.debug(LOG_STR, 'clicked accept btn')
    const result = await reportAcceptance()
    console.log(LOG_STR, "consent accepted", result)
    // console.log(LOG_STR, "consent remember:", rememberAcceptance())
    removeConsentElement(this)
}
function closeConsent(e) {
    removeConsentElement(this)
    console.log(LOG_STR, "consent closed by", this)
}

console.debug(LOG_STR, 'found accept button', acptBtn)
console.debug(LOG_STR, 'found close button', closBtn)

acptBtn?.addEventListener('click', acceptCoookies)
closBtn?.addEventListener('click', closeConsent);
