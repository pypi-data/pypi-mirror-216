function Footer() {
  return (
    <footer>
      <div
        style={{
          textAlign: "center",
          opacity: 0.25,
          fontFamily: [
            "Open Sans",
            "Helvetica Neue",
            "Helvetica",
            "Arial",
            "sans-serif",
          ],
        }}
      >
        <p>
          Made with
          <img
            src="images/Veles-logo-black.svg"
            style={{
              display: "inline",
              height: 1.5 + "em",
              verticalAlign: "baseline",
            }}
          />
        </p>
      </div>
    </footer>
  );
}

export default Footer;
