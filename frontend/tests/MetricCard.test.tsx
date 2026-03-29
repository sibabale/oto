import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { MetricCard } from "@/components/MetricCard";

describe("MetricCard", () => {
  it("renders label and value", () => {
    render(<MetricCard label="Net Margin" value="18.3%" />);

    expect(screen.getByText("Net Margin")).toBeInTheDocument();
    expect(screen.getByText("18.3%")).toBeInTheDocument();
  });
});
