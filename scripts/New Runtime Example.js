/** CONFIGURATION **/
var elementWaitTimer = 10000;

const url_to_monitor = 'https://www.tutorialrepublic.com/snippets/preview.php?topic=bootstrap&file=simple-login-form';
const user = 'keagan1';
const pass = 'test';
/** CONFIGURATION **/

async function stepOne() { //get homepage + validate element on page
  var loginHeaderXpath = "//h2[text()='Log in']";

  try {
    console.log('Hitting tutorial site: https://www.tutorialrepublic.com/');
    await $webDriver.get(url_to_monitor); //get url
    console.log("Switching to iFrame 'preview'");
    await $webDriver.wait($selenium.until.ableToSwitchToFrame($selenium.By.id('preview')), elementWaitTimer); //switch to iFrame where our validation element is nested within
    console.log('Attempting to validate: ' + loginHeaderXpath);
    await $webDriver.wait($selenium.until.elementLocated($selenium.By.xpath(loginHeaderXpath)), elementWaitTimer, 'Failed to locate element: ' + loginHeaderXpath)
    await $webDriver.findElement($selenium.By.xpath(loginHeaderXpath)); //find element on page
  } catch (e) {
    console.log('Step 1 Failure');
    $webDriver.takeScreenshot();
    $util.insights.set('Homepage Validation', 'FAILED');
    throw e;
  }
}

async function stepTwo() { //fill in login details on form + click submit
  var userXpath = "//input[@placeholder='Username']";
  var passXpath = "//input[@placeholder='Password']";
  var loginXpath = "//button[text() = 'Log in']";

  try {
    console.log('Locating userName InputBox');
    let userNameElement = await $webDriver.findElement($selenium.By.xpath(userXpath));
    console.log('Inputting userName');
    await userNameElement.sendKeys(user);
    console.log('Locating password InputBox');
    let passwordElement = await $webDriver.findElement($selenium.By.xpath(passXpath));
    console.log('Inputting password');
    await passwordElement.sendKeys(pass);
    console.log('Locating Log In button');
    let loginBtn = await $webDriver.findElement($selenium.By.xpath(loginXpath));
    console.log('Clicking Log In button');
    await loginBtn.click();
  } catch(e) {
    console.log('Step 2 Failure');
    $webDriver.takeScreenshot();
    $util.insights.set('Login Process', 'FAILED');
    throw e;
  }

}

async function stepThree() { //validate confirmation page
  var confirmationXpath = "//h1[text() = 'Confirmation']";

  try {
    console.log('Attempting to validate: ' + confirmationXpath);
    await $webDriver.wait($selenium.until.elementLocated($selenium.By.xpath(confirmationXpath)), elementWaitTimer, 'Failed to locate element: ' + confirmationXpath); //wait for element to be located on page (instead of using sleep)
    await $webDriver.findElement($selenium.By.xpath(confirmationXpath)); //find element on page
  } catch(e) {
    console.log('Step 3 Failure');
    $webDriver.takeScreenshot();
    $util.insights.set('Confirmation Validation', 'FAILED');
    throw e;
  }
}

async function main() {
  await stepOne();
  await stepTwo();
  await stepThree();
  console.log('complete');
}

main()
