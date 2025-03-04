import React from "react";
import { Accordion, AccordionHeader, AccordionBody } from "@material-tailwind/react";

const Footer = () => {
  return (
    <div className="bg-gray-800 text-white p-4">
      <Accordion>
        <AccordionHeader className="text-center">About Lex-AI</AccordionHeader>
        <AccordionBody className="justify-center flex text-gray-100 text-lg">
          &copy; 2023. Lex-AI. All rights reserved.
        </AccordionBody>
      </Accordion>
    </div>
  );
};

export default Footer;
