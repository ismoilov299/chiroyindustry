import PhoneInput from "react-phone-number-input";
import "react-phone-number-input/style.css";
import { zodResolver } from "@hookform/resolvers/zod";
import Section from "@/components/ui/section";
import Title from "@/components/ui/title";
import { useForm } from "react-hook-form";
import { FormSchema, formSchema } from "./form";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

const Contact = () => {
  const form = useForm<FormSchema>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      address: "",
      name: "",
    },
  });

  function onSubmit(values: FormSchema) {
    // Do something with the form values.
    // ✅ This will be type-safe and validated.
    console.log(values);
  }

  const handleActive = () => {
    const phoneValue = form.getValues("phone");
    if (!phoneValue) {
      form.setValue("phone", "+");
    }
  };

  return (
    <Section id="contact">
      <div className="flex items-center sm:flex-row flex-col">
        <div className="sm:w-1/2">
          <div className="flex flex-col items-center">
            <Title>Contact</Title>
            <div className="max-w-[600px] w-full mt-10">
              <Form {...form}>
                <form
                  onSubmit={form.handleSubmit(onSubmit)}
                  className="space-y-3"
                >
                  <FormField
                    control={form.control}
                    name="name"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Name</FormLabel>
                        <FormControl>
                          <Input placeholder="Name" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <FormField
                    control={form.control}
                    name="phone"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Phone</FormLabel>
                        <FormControl>
                          <PhoneInput
                            defaultCountry="UZ"
                            onFocus={handleActive}
                            className="phone-input !block"
                            placeholder={"Phone"}
                            value={field.value}
                            onChange={field.onChange}
                            inputComponent={Input}
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <FormField
                    control={form.control}
                    name="address"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Adress</FormLabel>
                        <FormControl>
                          <Input placeholder="Address" {...field} />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <FormField
                    control={form.control}
                    name="quantity"
                    render={({ field }) => (
                      <FormItem>
                        <FormLabel>Quantity</FormLabel>
                        <FormControl>
                          <Input
                            placeholder="Quantity"
                            type="number"
                            {...field}
                          />
                        </FormControl>
                        <FormMessage />
                      </FormItem>
                    )}
                  />
                  <Button className="w-full" type="submit">
                    Submit
                  </Button>
                </form>
              </Form>
            </div>
          </div>
        </div>
        <div className="sm:w-1/2 sm:block hidden">
          <div className="flex justify-center">
            <div className="max-w-96 overflow-hidden rounded-2xl">
              <img
                src="https://preview.colorlib.com/theme/pato/images/booking-01.jpg.webp"
                alt=""
                className="w-full h-full"
              />
            </div>
          </div>
        </div>
      </div>
    </Section>
  );
};

export default Contact;
